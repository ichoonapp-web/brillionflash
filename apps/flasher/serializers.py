from rest_framework import serializers
from .models import LightPreset

class LightPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightPreset
        fields = '__all__'
