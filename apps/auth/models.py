from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    credits = models.IntegerField(default=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=15, blank=True, null=True)
    purchased_items = models.JSONField(default=list)
    api_keys = models.ManyToManyField('ai.UserAPIKey', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']