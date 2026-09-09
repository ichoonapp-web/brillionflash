import os, stripe, openai, json, re
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
