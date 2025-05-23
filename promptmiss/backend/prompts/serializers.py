from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Prompt, Execution, Comment, Tag, PromptTag

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ['prompt']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_replies(self, obj):
        child_comments = Comment.objects.filter(parent=obj).order_by('created_at')
        return CommentSerializer(child_comments, many=True, context=self.context).data


class PromptSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = ['id', 'title', 'content', 'user', 'created_at', 'comments', 'like_count', 'bookmark_count', 'is_liked', 'is_bookmarked', 'tags']
        read_only_fields = ['user']

    def get_like_count(self, obj):
        return obj.prompt_likes.count()

    def get_bookmark_count(self, obj):
        return obj.bookmarks.count()

    def get_comments(self, obj):
        comments = obj.comments.order_by('-created_at')
        return CommentSerializer(comments, many=True, context=self.context).data

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

    def get_tags(self, obj):
        return [pt.tag.name for pt in PromptTag.objects.filter(prompt=obj)]

    def create(self, validated_data):
        prompt = Prompt.objects.create(**validated_data)
        tags = self.initial_data.get('tags', [])
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            PromptTag.objects.create(prompt=prompt, tag=tag)
        return prompt

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        tags = self.initial_data.get('tags', [])
        PromptTag.objects.filter(prompt=instance).delete()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            PromptTag.objects.create(prompt=instance, tag=tag)

        return instance


class ExecutionSerializer(serializers.ModelSerializer):
    prompt = PromptSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Execution
        fields = '__all__'