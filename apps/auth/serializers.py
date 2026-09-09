from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'credits', 'balance', 'phone', 'daily_streak', 'last_reward_date']
        read_only_fields = ['id', 'credits', 'balance', 'daily_streak', 'last_reward_date']

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        username = validated_data.get('username', email)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **validated_data
        )
        return user
