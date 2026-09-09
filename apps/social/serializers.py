from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_email', 'text', 'image', 'created_at', 'likes']

class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_email', 'text', 'created_at']
