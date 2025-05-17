from django.contrib.auth import get_user_model
from django.db import models

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
    user_input = models.TextField()
    result = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Execution of '{self.prompt.title}' at {self.executed_at}"