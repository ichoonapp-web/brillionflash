from django.db import models
from django.conf import settings

class LightPreset(models.Model):
    name = models.CharField(max_length=100)
    red = models.IntegerField(default=255)
    green = models.IntegerField(default=255)
    blue = models.IntegerField(default=255)
    brightness = models.IntegerField(default=100)
    kelvin = models.IntegerField(default=6500)
    mode = models.CharField(max_length=20, choices=[
        ('direct', 'Direct'),
        ('ambient', 'Ambient'),
        ('combined', 'Combined'),
    ], default='combined')
    is_trending = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
