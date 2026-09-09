from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    credits = models.IntegerField(default=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=15, blank=True, null=True)
    purchased_items = models.JSONField(default=list)
    api_keys = models.ManyToManyField('ai.UserAPIKey', blank=True)
    daily_streak = models.IntegerField(default=0)
    last_reward_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def claim_daily_reward(self):
        today = timezone.now().date()
        if self.last_reward_date == today:
            return False, "Daily reward already claimed today", 0

        if self.last_reward_date == today - timedelta(days=1):
            self.daily_streak += 1
        else:
            self.daily_streak = 1

        reward_credits = min(self.daily_streak, 5)
        self.credits += reward_credits
        self.last_reward_date = today
        self.save()
        return True, f"Claimed +{reward_credits} credits for Day {self.daily_streak} streak!", reward_credits
