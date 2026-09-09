import stripe
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Item
from .serializers import ItemSerializer

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        item_id = data['itemId']
        item = Item.objects.get(id=item_id)
        buyer = request.user
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.title},
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
            metadata={'item_id': str(item.id), 'buyer_id': str(buyer.id)}
        )
        return JsonResponse({'url': session.url})
