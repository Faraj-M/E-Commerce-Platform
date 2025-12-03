import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if hasattr(order, 'payment'):
        messages.info(request, 'Payment already exists for this order.')
        return redirect('order_detail', order_id=order.id)
    
    if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY.startswith('sk_test_51QEXAMPLE'):
        messages.error(request, 'Stripe API keys are not configured. Please add your Stripe keys to the .env file and restart Docker with: docker-compose -f infrastructure/docker-compose.yml restart web')
        return redirect('order_detail', order_id=order.id)
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency='usd',
            metadata={'order_id': order.id},
        )
        
        payment = Payment.objects.create(
            order=order,
            stripe_payment_intent_id=intent.id,
            amount=order.total_amount,
            status='pending',
        )
        
        context = {
            'order': order,
            'payment': payment,
            'client_secret': intent.client_secret,
            'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, 'payments/payment.html', context)
    
    except Exception as e:
        messages.error(request, f'Error creating payment: {str(e)}')
        return redirect('order_detail', order_id=order.id)


@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, order__user=request.user)
    
    # Update payment and order status when payment succeeds
    if payment.status == 'pending':
        try:
            # Verify payment with Stripe
            intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)
            if intent.status == 'succeeded':
                payment.status = 'succeeded'
                payment.save()
                payment.order.status = 'processing'
                payment.order.save()
                messages.success(request, 'Payment successful! Your order is being processed.')
            elif intent.status == 'requires_payment_method':
                payment.status = 'failed'
                payment.save()
                messages.error(request, 'Payment failed. Please try again.')
        except Exception as e:
            messages.warning(request, f'Payment verification issue: {str(e)}')
    
    context = {'payment': payment}
    return render(request, 'payments/success.html', context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            payment.status = 'succeeded'
            payment.save()
            payment.order.status = 'processing'
            payment.order.save()
        except Payment.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    return HttpResponse(status=200)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=self.request.user)
