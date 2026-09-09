from django.db import models
from django.conf import settings

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    sales = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default='light')