from django.urls import path
from .views import PresetListCreateView, PresetRetrieveUpdateDestroyView, TrendingPresetsView
urlpatterns = [
    path('presets/', PresetListCreateView.as_view()),
    path('presets/<int:pk>/', PresetRetrieveUpdateDestroyView.as_view()),
    path('trending/', TrendingPresetsView.as_view()),
]
