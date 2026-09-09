from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.marketplace.models import Item
from apps.auth.models import User
from datetime import timedelta

class AnalyticsDashboardView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        data = {
            'total_users': User.objects.count(),
            'new_users_this_week': User.objects.filter(date_joined__gte=week_ago).count(),
            'total_items': Item.objects.count(),
            'total_sales': Item.objects.aggregate(total_sales=Sum('sales'))['total_sales'],
            'total_views': Item.objects.aggregate(total_views=Sum('views'))['total_views'],
            'recent_items': list(Item.objects.order_by('-created_at')[:10].values('id', 'title', 'price', 'sales')),
        }
        return Response(data)