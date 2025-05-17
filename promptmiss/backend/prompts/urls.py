from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromptViewSet, ExecutionViewSet

router = DefaultRouter()
router.register('prompts', PromptViewSet)
router.register('executions', ExecutionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]