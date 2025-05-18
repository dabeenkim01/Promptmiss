from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

User = get_user_model()

class Prompt(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Execution(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    result = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Execution of '{self.prompt.title}' at {self.executed_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='prompt_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'prompt')

    def __str__(self):
        return f'{self.user.username} likes {self.prompt.title}'


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'prompt')

    def __str__(self):
        return f'{self.user.username} bookmarked {self.prompt.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content[:20]}'


class PromptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Prompt
        fields = ['id', 'title', 'content', 'tags', 'user', 'created_at']