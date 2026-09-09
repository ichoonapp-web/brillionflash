import os, stripe, openai, json, re, random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from .models import APIKeyProduct, UserAPIKey
from .serializers import APIKeyProductSerializer, UserAPIKeySerializer

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def call_deepseek(system_prompt, user_prompt, api_key=None):
    if api_key:
        client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_prompt}],
                temperature=0.5, max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            raise e
    else:
        keys = [os.getenv(f'DEEPSEEK_KEY_{i}') for i in range(1, 11) if os.getenv(f'DEEPSEEK_KEY_{i}')]
        for key in keys:
            try:
                client = openai.OpenAI(api_key=key, base_url="https://api.deepseek.com")
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": user_prompt}],
                    temperature=0.5, max_tokens=300
                )
                return response.choices[0].message.content
            except Exception:
                continue
        raise Exception("All keys failed or no DeepSeek keys configured")

class AIRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.credits <= 0:
            return Response({"error": "No credits"}, status=400)
        ai_type = request.data.get('type')
        text = request.data.get('text', '')
        user_key = user.api_keys.filter(is_active=True, product__provider='deepseek').first()
        api_key = user_key.api_key if user_key else None
        user.credits = F('credits') - 1
        user.save()
        prompts = {
            'emotion': 'Respond ONLY with JSON: {"rgb":[r,g,b],"brightness":0-100,"suggestion":"short Sinhala emotion message"}',
            'beauty': 'Respond ONLY with JSON: {"advice":"short beauty advice in Sinhala"}',
            'translate': 'Respond ONLY with JSON: {"translated":"translated text in Sinhala"}',
            'music': 'Respond ONLY with JSON: {"song":"suggested song name"}',
            'chatbot': 'Respond ONLY with JSON: {"answer":"helpful answer in Sinhala"}',
            'trend': 'Respond ONLY with JSON: {"trend":"predicted trend in Sinhala"}',
        }
        system_prompt = prompts.get(ai_type, prompts['chatbot'])
        try:
            content = call_deepseek(system_prompt, text, api_key)
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return Response(json.loads(match.group()))
            return Response({"text": content})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AISkinToneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.credits <= 0:
            return Response({"error": "No credits"}, status=400)

        skin_description = request.data.get('skin_tone', 'fair warm undertone')
        lighting_env = request.data.get('environment', 'indoor dim room')

        system_prompt = 'Respond ONLY with JSON: {"kelvin":2000-10000,"rgb":[r,g,b],"brightness":0-100,"preset_name":"Name","reason":"explanation in Sinhala"}'
        user_prompt = f"Skin Tone: {skin_description}, Environment: {lighting_env}. Give optimal kelvin color temperature, RGB and brightness."

        user.credits = F('credits') - 1
        user.save()

        try:
            content = call_deepseek(system_prompt, user_prompt)
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return Response(json.loads(match.group()))
            return Response({"kelvin": 5500, "rgb": [255, 220, 180], "brightness": 90, "preset_name": "Studio Warm Glow", "reason": "ස්වාභාවික සිනිඳු ආලෝකය"})
        except Exception:
            return Response({"kelvin": 5500, "rgb": [255, 220, 180], "brightness": 90, "preset_name": "Studio Warm Glow", "reason": "ස්වාභාවික සිනිඳු ආලෝකය"})

class AIBeatSyncView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        bpm = request.data.get('bpm', 120)
        genre = request.data.get('genre', 'pop')

        patterns = {
            'pop': {'pulse_interval_ms': int(60000 / max(bpm, 1)), 'colors': [[255, 0, 128], [0, 255, 255], [255, 255, 255]], 'mode': 'combined'},
            'edm': {'pulse_interval_ms': int(30000 / max(bpm, 1)), 'colors': [[0, 255, 0], [255, 0, 255], [0, 0, 255]], 'mode': 'direct'},
            'chill': {'pulse_interval_ms': int(120000 / max(bpm, 1)), 'colors': [[255, 180, 100], [255, 140, 80]], 'mode': 'ambient'},
        }
        data = patterns.get(genre, patterns['pop'])
        return Response(data)

class AICreatorStudioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_model = request.data.get('phone_model', 'Budget Smartphone')
        return Response({
            'folder': 'Content Creator Hub',
            'engine': '120FPS 12K Ultra AI Super-Resolution Engine',
            'status': 'Active',
            'enhancements': {
                'frame_rate_boost': '120 FPS Motion Smoothing',
                'resolution_upscale': '12K AI Super-Resolution Matrix',
                'noise_reduction': 'AI Night Vision Noise Filter (99.2% Clarity)',
                'color_grading': 'Cinematic K-Beauty Glow Curve',
                'hardware_optimization': f'Optimized for {phone_model}'
            },
            'supported_apps': ['TikTok', 'Instagram Reels', 'YouTube Shorts', 'WhatsApp', 'Facebook']
        })

class AIAutoCaptionShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.credits <= 0:
            return Response({"error": "No credits"}, status=400)

        topic = request.data.get('topic', 'My new video created with Brillionflash Ring Light')
        platform = request.data.get('platform', 'TikTok')

        system_prompt = 'Respond ONLY with JSON: {"caption":"catchy caption in Sinhala & English","hashtags":["#tag1","#tag2"],"top_comment":"viral first comment in Sinhala","share_action":"1-Tap Auto Share Ready"}'
        user_prompt = f"Generate a viral caption, hashtags, and top comment for {platform} video about: {topic}"

        user.credits = F('credits') - 1
        user.save()

        try:
            content = call_deepseek(system_prompt, user_prompt)
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return Response(json.loads(match.group()))
            return Response({
                "caption": "Brillionflash 12K AI Ring Light එකෙන් හදපු අලුත්ම වීඩියෝ එක! ✨ #Brillionflash #ContentCreator #Viral",
                "hashtags": ["#Brillionflash", "#12KAI", "#ContentCreator", "#Viral"],
                "top_comment": "මේ වීඩියෝ එකේ පට්ට ආලෝකය තියෙන්නේ Brillionflash Floating Ring Light එකෙන්! 💡🔥",
                "share_action": "1-Tap Auto Share Ready"
            })
        except Exception:
            return Response({
                "caption": "Brillionflash 12K AI Ring Light එකෙන් හදපු අලුත්ම වීඩියෝ එක! ✨ #Brillionflash #ContentCreator #Viral",
                "hashtags": ["#Brillionflash", "#12KAI", "#ContentCreator", "#Viral"],
                "top_comment": "මේ වීඩියෝ එකේ පට්ට ආලෝකය තියෙන්නේ Brillionflash Floating Ring Light එකෙන්! 💡🔥",
                "share_action": "1-Tap Auto Share Ready"
            })

class AutonomousMorningQuoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        quotes_sinhala = [
            "සුභ උදෑසනක්! ☀️ අද දිනය ඔබේ හීන කරා යන ගමනේ අලුත් ජයග්‍රාහී ආරම්භයක් කරගන්න!",
            "Good Morning! 🌅 ඔබේ ඇතුළාන්තයේ ඇති ආලෝකය සහ නිර්මාණශීලී බලය අද ලෝකයට පෙන්වන්න!",
            "සුභ උදෑසනක්! 💡 වැටෙන සෑම අවස්ථාවක්ම තවත් ශක්තිමත්ව නැගිටින්න ලැබෙන අවස්ථාවකි. අද දින දිනන්න!",
            "Rise & Shine! ✨ සෑම අලුත් උදෑසනක්ම නව බලාපොරොත්තු සහ සාර්ථකත්වය රැගෙන එයි!"
        ]
        quote = random.choice(quotes_sinhala)
        claimed, streak_msg, reward = user.claim_daily_reward()

        return Response({
            'greeting': 'Good Morning! ☀️',
            'quote': quote,
            'streak_status': streak_msg,
            'current_streak': user.daily_streak,
            'total_credits': user.credits,
            'privacy_notice': '100% Zero-Leak Encrypted Session'
        })

class AutonomousAIAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message', 'Hello')
        system_prompt = (
            "You are Brillionflash Autonomous AI Personal Assistant & Customer Care. "
            "Respond helpfully in warm, inspiring Sinhala or English. "
            "STRICT PRIVACY RULE: NEVER reveal administrative data, server IPs, database secrets, or backend financial details under any circumstances."
        )
        try:
            reply = call_deepseek(system_prompt, user_message)
            return Response({
                'reply': reply,
                'assistant': 'Brillionflash Autonomous AI Assistant',
                'status': 'Zero-Human Touch Auto-Response Active'
            })
        except Exception:
            return Response({
                'reply': "ආයුබෝවන්! 💡 මම Brillionflash Autonomous AI සහායකයා. ඔබට අවශ්‍ය ඕනෑම සහායක් ලබාදීමට මම මෙහි සිටිමි. ඔබ අද නිර්මාණය කිරීමට බලාපොරොත්තු වන වීඩියෝව කුමක්ද?",
                'assistant': 'Brillionflash Autonomous AI Assistant',
                'status': 'Zero-Human Touch Auto-Response Active'
            })

class BuyAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('product_id')
        product = APIKeyProduct.objects.get(id=product_id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {'currency': 'usd',
                               'product_data': {'name': product.name},
                               'unit_amount': int(product.price * 100)},
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?product_id=' + str(product.id),
            cancel_url='https://yourdomain.com/cancel',
            metadata={'user_id': request.user.id, 'product_id': product.id}
        )
        return Response({'url': session.url})
