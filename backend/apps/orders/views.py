from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.catalog.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


def get_cart(request):
    cart = request.session.get('cart', {})
    return cart


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = get_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity
        
        if cart[str(product_id)] > product.stock_quantity:
            cart[str(product_id)] = product.stock_quantity
            messages.warning(request, f'Only {product.stock_quantity} items available in stock.')
        
        request.session['cart'] = cart
        messages.success(request, f'{product.name} added to cart.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'{product.name} added to cart.'})
        
        return redirect('product_detail', slug=product.slug)
    
    return redirect('product_list')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)
        quantity = int(request.POST.get('quantity', 0))
        product = get_object_or_404(Product, id=product_id)
        
        if quantity <= 0:
            if str(product_id) in cart:
                del cart[str(product_id)]
        else:
            if quantity > product.stock_quantity:
                quantity = product.stock_quantity
                messages.warning(request, f'Only {product.stock_quantity} items available.')
            cart[str(product_id)] = quantity
        
        request.session['cart'] = cart
        return redirect('cart_view')
    
    return redirect('cart_view')


def cart_view(request):
    cart = get_cart(request)
    cart_items = []
    total = Decimal('0.00')
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
        except Product.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_view')
    
    if request.method == 'POST':
        user = request.user
        cart_items = []
        total = Decimal('0.00')
        
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id, is_active=True)
            if quantity > product.stock_quantity:
                messages.error(request, f'Insufficient stock for {product.name}.')
                return redirect('cart_view')
            
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
            })
        
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        shipping_country = request.POST.get('shipping_country')
        
        if not all([shipping_address, shipping_city, shipping_postal_code, shipping_country]):
            messages.error(request, 'Please fill in all shipping details.')
            return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})
        
        order = Order.objects.create(
            user=user,
            total_amount=total,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_country=shipping_country,
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )
            item['product'].stock_quantity -= item['quantity']
            item['product'].save()
        
        request.session['cart'] = {}
        request.session['order_id'] = order.id
        return redirect('payment_create', order_id=order.id)
    
    cart_items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id, is_active=True)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        items = order.items.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)
