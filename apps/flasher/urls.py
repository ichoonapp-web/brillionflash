from django.urls import path
from .views import PresetListCreateView, PresetRetrieveUpdateDestroyView, TrendingPresetsView, InstantOneTapGlowView

urlpatterns = [
    path('presets/', PresetListCreateView.as_view()),
    path('presets/<int:pk>/', PresetRetrieveUpdateDestroyView.as_view()),
    path('trending/', TrendingPresetsView.as_view()),
    path('instant-glow/', InstantOneTapGlowView.as_view()),
]
