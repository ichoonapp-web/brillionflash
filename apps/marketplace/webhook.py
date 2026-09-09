import stripe, os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = stripe.Webhook.construct_event(payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET'))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if 'product_id' in session.metadata:
            # API Key purchase
            from apps.ai.models import APIKeyProduct, UserAPIKey
            user_id = session.metadata['user_id']
            product = APIKeyProduct.objects.get(id=session.metadata['product_id'])
            for _ in range(product.key_count):
                UserAPIKey.objects.create(user_id=user_id, product=product, api_key=os.getenv('DEEPSEEK_KEY_1'))
        else:
            # Item purchase
            item_id = session.metadata['item_id']
            buyer_id = session.metadata['buyer_id']
            item = Item.objects.get(id=item_id)
            buyer = settings.AUTH_USER_MODEL.objects.get(id=buyer_id)
            seller = item.creator
            admin = settings.AUTH_USER_MODEL.objects.get(id=os.getenv('ADMIN_UID'))
            # 30/70 split
            seller.balance += item.price * 0.7
            seller.save()
            admin.balance += item.price * 0.3
            admin.save()
            buyer.purchased_items.append(item_id)
            buyer.save()
            item.sales += 1
            item.save()
    return JsonResponse({'status': 'ok'})