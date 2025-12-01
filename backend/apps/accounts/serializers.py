from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'city', 'postal_code', 'country',
            'date_joined', 'created_at'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at']
