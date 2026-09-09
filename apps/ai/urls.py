from django.urls import path
from .views import (
    AIRequestView, BuyAPIKeyView, AISkinToneView, AIBeatSyncView,
    AICreatorStudioView, AIAutoCaptionShareView, AutonomousMorningQuoteView,
    AutonomousAIAssistantView
)

urlpatterns = [
    path('request/', AIRequestView.as_view()),
    path('skin-tone/', AISkinToneView.as_view()),
    path('beat-sync/', AIBeatSyncView.as_view()),
    path('creator-studio/', AICreatorStudioView.as_view()),
    path('auto-caption/', AIAutoCaptionShareView.as_view()),
    path('morning-quote/', AutonomousMorningQuoteView.as_view()),
    path('autonomous-assistant/', AutonomousAIAssistantView.as_view()),
    path('buy-key/', BuyAPIKeyView.as_view()),
]
