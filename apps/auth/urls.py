from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView, DailyRewardView, AboutAppView, DownloadAabView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('daily-reward/', DailyRewardView.as_view()),
    path('about-app/', AboutAppView.as_view()),
    path('download-aab/', DownloadAabView.as_view()),
]
