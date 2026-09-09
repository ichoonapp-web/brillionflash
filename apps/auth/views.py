import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse, FileResponse
from pathlib import Path
from .serializers import UserSerializer

User = get_user_model()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email') or request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is None and email:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class DailyRewardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        success, message, reward = request.user.claim_daily_reward()
        if success:
            return Response({
                'success': True,
                'message': message,
                'credits_rewarded': reward,
                'current_streak': request.user.daily_streak,
                'total_credits': request.user.credits
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': message,
            'current_streak': request.user.daily_streak,
            'total_credits': request.user.credits
        }, status=status.HTTP_400_BAD_REQUEST)

class AboutAppView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'app_name': 'Brillionflash Global #1 AI Emotion Light & Creator Studio',
            'version': '3.0.0+21',
            'tagline': 'Global #1 AI Lighting & Creator Monetization Platform',
            'user_benefits': [
                {
                    'step': '1. Flagship 12K 120FPS Quality on Normal Phones',
                    'title': 'සාමාන්‍ය Phone එකකින් $1200 Pro Studio Quality ලබාගැනීම',
                    'description': '120 FPS Motion Smoothing, 12K AI Super-Resolution, සහ AI Night Vision Noise Reduction මගින් ඕනෑම සරල Phone එකක කැමරාව Pro Studio එකක් බවට පත් කරයි.'
                },
                {
                    'step': '2. Floating Ring Light Multitasking Over ALL Apps',
                    'title': 'ලෝකයේ ඕනෑම App එකක් (TikTok/Reels/Zoom) මත Floating Ring Light භාවිතය',
                    'description': 'TikTok, Instagram, Camera, Zoom හෝ WhatsApp භාවිත කරන අතරතුර Screen එක මත පාවෙන Floating Ring Light එකෙන් Kelvin warm/cool ආලෝකය වෙනස් කළ හැක.'
                },
                {
                    'step': '3. How Users Can Earn Money (Creator Monetization)',
                    'title': 'පරිශීලකයින්ට මුදල් ඉපැයීමේ අවස්ථා (Earn Cash as a Creator)',
                    'description': 'ඔබ සාදන Custom Light Presets Brillionflash Marketplace හි විකිණීමට තබා 70% ක කෙලින්ම ආදායමක් ඔබේ බැංකු ගිණුමට ලබාගන්න!'
                },
                {
                    'step': '4. Free Daily AI Credits & Rewarded Rewards',
                    'title': 'නොමිලේ AI Credits සහ Daily Streak Rewards',
                    'description': 'දිනපතා App එකට ලොග් වී නොමිලේ Free AI Credits හිමිකර ගන්න. Ads බැලීමෙන් තවත් AI Credits එකතු කරගන්න.'
                },
                {
                    'step': '5. 1-Tap Viral Auto-Caption & Social Sharing',
                    'title': '1-Tap Auto-Captioning සහ Viral Hashtag Generator',
                    'description': 'TikTok, Reels, Shorts සඳහා AI මගින් Captions සහ Hashtags එක ක්ලික් එකෙන් සාදා කෙලින්ම Share කරන්න.'
                }
            ],
            'autonomous_status': '100% Zero-Human Touch Operations Active',
            'privacy_guarantee': '100% Encrypted & Private - Zero Data Leak'
        })

class DownloadAabView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        file_path = os.path.join(BASE_DIR, 'static', 'brillionflash-release.aab')
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='brillionflash-release.aab')
        else:
            response = HttpResponse("Brillionflash Release AAB Package Download Endpoint.", content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="brillionflash-release-v3.0.0.aab"'
            return response
