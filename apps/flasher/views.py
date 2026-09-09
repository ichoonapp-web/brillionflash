from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import LightPreset
from .serializers import LightPresetSerializer

class PresetListCreateView(generics.ListCreateAPIView):
    queryset = LightPreset.objects.all()
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]

class PresetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LightPreset.objects.all()
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]

class TrendingPresetsView(generics.ListAPIView):
    serializer_class = LightPresetSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return LightPreset.objects.filter(is_trending=True).order_by('-id')[:20]
