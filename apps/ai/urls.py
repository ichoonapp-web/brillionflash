from django.urls import path
from .views import AIRequestView, BuyAPIKeyView, AISkinToneView, AIBeatSyncView

urlpatterns = [
    path('request/', AIRequestView.as_view()),
    path('skin-tone/', AISkinToneView.as_view()),
    path('beat-sync/', AIBeatSyncView.as_view()),
    path('buy-key/', BuyAPIKeyView.as_view()),
]
