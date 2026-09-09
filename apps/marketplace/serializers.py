from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    creator_email = serializers.ReadOnlyField(source='creator.email')
    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'price', 'image', 'creator', 'creator_email', 'created_at', 'rating', 'sales', 'views', 'category']
