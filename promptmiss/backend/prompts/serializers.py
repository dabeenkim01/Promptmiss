from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Prompt, Execution, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['prompt']


class PromptSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # 작성자의 ID만 반환

    class Meta:
        model = Prompt
        fields = ['id', 'title', 'content', 'tags', 'user', 'created_at', 'comments', 'like_count', 'bookmark_count', 'is_liked', 'is_bookmarked']  # is_bookmarked will be included as SerializerMethodField
        read_only_fields = ['user']

    def get_like_count(self, obj):
        return obj.prompt_likes.count()

    def get_bookmark_count(self, obj):
        return obj.bookmarks.count()

    def get_comments(self, obj):
        comments = obj.comments.order_by('-created_at')
        return CommentSerializer(comments, many=True).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj.prompt_likes.filter(user=user).exists()
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj.bookmarks.filter(user=user).exists()
        return False


class ExecutionSerializer(serializers.ModelSerializer):
    prompt = PromptSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Execution
        fields = '__all__'