from django.db import models
from django.conf import settings

class APIKeyProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    key_count = models.IntegerField(default=1)
    provider = models.CharField(max_length=20, default='deepseek')
    is_active = models.BooleanField(default=True)

class UserAPIKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(APIKeyProduct, on_delete=models.SET_NULL, null=True)
    api_key = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.api_key[:8]}..."