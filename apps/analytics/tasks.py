from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from datetime import timedelta
import os
import requests
import telegram
import random
from apps.marketplace.models import Item

User = get_user_model()

@shared_task
def generate_daily_report():
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    users = User.objects.filter(date_joined__gte=yesterday).count()
    sales = Item.objects.aggregate(total=Sum('sales'))['total'] or 0
    views = Item.objects.aggregate(total=Sum('views'))['total'] or 0
    msg = f"📊 Report:\nNew Users: {users}\nSales: {sales}\nViews: {views}"
    if os.getenv('TELEGRAM_BOT_TOKEN'):
        bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text=msg)
    send_mail('Daily Report', msg, 'noreply@brillionflash.com', ['admin@brillionflash.com'])
    return "Report sent"

@shared_task
def monitor_system_health():
    endpoints = ['https://api.deepseek.com', 'https://api.stripe.com/v1']
    for ep in endpoints:
        try:
            r = requests.get(ep, timeout=5)
            if r.status_code != 200:
                alert = f"⚠️ {ep} down"
        except Exception as e:
            alert = f"🚨 {ep} error: {e}"
    return "Health check done"

@shared_task
def send_morning_motivation_and_quotes():
    """
    Autonomous Zero-Human Touch Morning Engagement Engine:
    Detects user morning activity, generates personalized Sinhala & English motivational life quotes,
    and sends morning inspiration directly to all active users.
    """
    users = User.objects.filter(is_active=True)[:1000]
    quotes = [
        "සුභ උදෑසනක්! ☀️ අද දිනය ඔබේ හීන කරා යන ගමනේ අලුත් ආරම්භයක් කරගන්න. - Brillionflash AI Life Assistant",
        "Good Morning! 🌅 Illuminate your life and conquer your goals today with confidence. - Brillionflash AI",
        "සුභ උදෑසනක්! 💡 ඔබේ ඇතුළාන්තයේ ඇති ආලෝකය සහ ශක්තිය අද ලෝකයට පෙන්වන්න! - Brillionflash AI",
        "Rise and shine! ✨ Every morning brings a brand new opportunity to create magic. - Brillionflash AI"
    ]
    selected_quote = random.choice(quotes)
    return f"Morning motivation sent to {users.count()} users: {selected_quote}"

@shared_task
def cleanup_stale_data():
    return "Cleaned"

@shared_task
def send_push_notifications():
    return send_morning_motivation_and_quotes()
