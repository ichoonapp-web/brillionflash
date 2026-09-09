from rest_framework import serializers
from .models import APIKeyProduct, UserAPIKey

class APIKeyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKeyProduct
        fields = '__all__'

class UserAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAPIKey
        fields = ['id', 'api_key', 'product', 'is_active', 'expires_at']
