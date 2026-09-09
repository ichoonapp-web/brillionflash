from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth.urls')),
    path('api/flasher/', include('apps.flasher.urls')),
    path('api/ai/', include('apps.ai.urls')),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/social/', include('apps.social.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]