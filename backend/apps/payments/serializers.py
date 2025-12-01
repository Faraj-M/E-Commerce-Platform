from rest_framework import serializers
from .models import Payment
from apps.orders.serializers import OrderSerializer


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'stripe_payment_intent_id', 'amount',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
