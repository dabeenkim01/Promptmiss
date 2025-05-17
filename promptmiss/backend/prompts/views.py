from rest_framework import viewsets
from .models import Prompt, Execution
from .serializers import PromptSerializer, ExecutionSerializer

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

class ExecutionViewSet(viewsets.ModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
