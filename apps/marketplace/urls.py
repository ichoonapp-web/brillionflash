from django.urls import path
from .views import ItemListCreateView, ItemRetrieveUpdateDestroyView, create_checkout_session
from .webhook import stripe_webhook
urlpatterns = [
    path('items/', ItemListCreateView.as_view()),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view()),
    path('checkout/', create_checkout_session),
    path('webhook/', stripe_webhook),
]
