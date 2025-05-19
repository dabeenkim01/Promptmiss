from django.urls import path
from . import views

urlpatterns = [
    path('prompts/', views.prompt_list_create, name='prompt-list-create'),
    path('prompts/<int:pk>/', views.prompt_detail, name='prompt-detail'),
    path('prompts/<int:pk>/like/', views.toggle_like, name='toggle-like'),
    path('prompts/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle-bookmark'),
    path('prompts/<int:pk>/execute/', views.execute_prompt, name='execute-prompt'),
    path('prompts/<int:prompt_id>/comments/', views.comment_list_create, name='comment-list-create'),
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment-delete'),
    path('comments/<int:comment_id>/like/', views.toggle_comment_like, name='comment-like'),
]