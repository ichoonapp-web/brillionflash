from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import LightPreset
from .serializers import LightPresetSerializer

class PresetListCreateView(generics.ListCreateAPIView):
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        qs = LightPreset.objects.all()
        if category:
            qs = qs.filter(category=category)
        if not qs.exists():
            self._seed_default_presets()
            qs = LightPreset.objects.all()
            if category:
                qs = qs.filter(category=category)
        return qs.order_by('-id')

    def _seed_default_presets(self):
        defaults = [
            {'name': 'K-Beauty Soft Glow', 'red': 255, 'green': 225, 'blue': 210, 'brightness': 95, 'kelvin': 5200, 'category': 'k_beauty', 'is_trending': True},
            {'name': 'Cinematic Warm Gold', 'red': 255, 'green': 190, 'blue': 120, 'brightness': 90, 'kelvin': 3200, 'category': 'cinematic_studio', 'is_trending': True},
            {'name': 'Cyberpunk Neon Pulse', 'red': 0, 'green': 240, 'blue': 255, 'brightness': 100, 'kelvin': 8500, 'category': 'cyberpunk_neon', 'is_trending': True},
            {'name': 'Soft Natural Portrait', 'red': 250, 'green': 240, 'blue': 230, 'brightness': 85, 'kelvin': 5600, 'category': 'soft_portrait', 'is_trending': True},
            {'name': 'TikTok Streamer Ring', 'red': 255, 'green': 210, 'blue': 240, 'brightness': 98, 'kelvin': 6000, 'category': 'tiktok_streamer', 'is_trending': True},
        ]
        for p in defaults:
            LightPreset.objects.get_or_create(name=p['name'], defaults=p)

class PresetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LightPreset.objects.all()
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]

class TrendingPresetsView(generics.ListAPIView):
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = LightPreset.objects.filter(is_trending=True)
        if not qs.exists():
            PresetListCreateView()._seed_default_presets()
            qs = LightPreset.objects.filter(is_trending=True)
        return qs.order_by('-id')[:20]
