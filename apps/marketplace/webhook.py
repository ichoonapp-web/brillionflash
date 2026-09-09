import stripe, os
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from apps.marketplace.models import Item

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')

    try:
        if webhook_secret and sig_header:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            import json
            event = json.loads(payload)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event.get('type') == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        User = get_user_model()

        if 'product_id' in metadata:
            from apps.ai.models import APIKeyProduct, UserAPIKey
            user_id = metadata['user_id']
            product = APIKeyProduct.objects.get(id=metadata['product_id'])
            for _ in range(product.key_count):
                UserAPIKey.objects.create(user_id=user_id, product=product, api_key=os.getenv('DEEPSEEK_KEY_1', 'default_key'))
        elif 'item_id' in metadata:
            item_id = metadata['item_id']
            buyer_id = metadata['buyer_id']
            item = Item.objects.get(id=item_id)
            buyer = User.objects.get(id=buyer_id)
            seller = item.creator

            admin_id = os.getenv('ADMIN_UID')
            admin = User.objects.filter(id=admin_id).first() if admin_id else None

            seller.balance += item.price * Decimal('0.7')
            seller.save()
            if admin:
                admin.balance += item.price * Decimal('0.3')
                admin.save()

            if isinstance(buyer.purchased_items, list):
                buyer.purchased_items.append(item_id)
            else:
                buyer.purchased_items = [item_id]
            buyer.save()

            item.sales += 1
            item.save()

    return JsonResponse({'status': 'ok'})
