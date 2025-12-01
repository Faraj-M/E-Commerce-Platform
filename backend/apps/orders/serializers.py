from rest_framework import serializers
from .models import Order, OrderItem
from apps.catalog.models import Product
from apps.catalog.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_amount', 'shipping_address',
            'shipping_city', 'shipping_postal_code', 'shipping_country',
            'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['created_at', 'updated_at']
