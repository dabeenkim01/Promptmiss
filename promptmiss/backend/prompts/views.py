from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Prompt, Execution
from .serializers import PromptSerializer, ExecutionSerializer

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Prompt.objects.all()
        if self.request.query_params.get('mine') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExecutionViewSet(viewsets.ModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
