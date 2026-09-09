from django.urls import path
from .views import PostListCreateView, PostRetrieveView, CommentListCreateView
urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveView.as_view()),
    path('comments/', CommentListCreateView.as_view()),
]
