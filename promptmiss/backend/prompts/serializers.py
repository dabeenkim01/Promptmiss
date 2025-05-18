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

    class Meta:
        model = Prompt
        fields = '__all__'
        read_only_fields = ['user']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_bookmark_count(self, obj):
        return obj.bookmarks.count()

    def get_comments(self, obj):
        comments = obj.comments.order_by('-created_at')
        return CommentSerializer(comments, many=True).data


class ExecutionSerializer(serializers.ModelSerializer):
    prompt = PromptSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Execution
        fields = '__all__'