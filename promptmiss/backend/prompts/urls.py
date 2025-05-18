"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromptViewSet, ExecutionViewSet, ToggleLikeView, ToggleBookmarkView, ExecutePromptView, CommentViewSet

router = DefaultRouter()
router.register('prompts', PromptViewSet)
router.register('executions', ExecutionViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('prompts/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('prompts/<int:pk>/bookmark/', ToggleBookmarkView.as_view(), name='toggle-bookmark'),
    path('prompts/<int:pk>/execute/', ExecutePromptView.as_view(), name='execute-prompt'),
]