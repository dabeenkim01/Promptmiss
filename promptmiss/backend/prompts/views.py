from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Prompt, Like, Bookmark, Comment, Tag, PromptTag
from .serializers import PromptSerializer, CommentSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def prompt_list_create(request):
    if request.method == 'GET':
        prompts = Prompt.objects.all()
        tag_name = request.query_params.get('tag')
        mine = request.query_params.get('mine')
        liked = request.query_params.get('liked')
        bookmarked = request.query_params.get('bookmarked')
        if tag_name:
            prompts = prompts.filter(prompttag__tag__name=tag_name)
        if mine == 'true' and request.user.is_authenticated:
            prompts = prompts.filter(user=request.user)
        elif liked == 'true' and request.user.is_authenticated:
            prompts = prompts.filter(prompt_likes__user=request.user)
        elif bookmarked == 'true' and request.user.is_authenticated:
            prompts = prompts.filter(bookmarks__user=request.user)

        serializer = PromptSerializer(prompts, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PromptSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def prompt_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)

    if request.method == 'GET':
        serializer = PromptSerializer(prompt, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != prompt.user:
            return Response({'detail': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PromptSerializer(prompt, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != prompt.user:
            return Response({'detail': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        prompt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, prompt=prompt)
    if not created:
        like.delete()
        return Response({'is_liked': False, 'like_count': prompt.prompt_likes.count()})
    return Response({'is_liked': True, 'like_count': prompt.prompt_likes.count()})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_bookmark(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, prompt=prompt)
    if not created:
        bookmark.delete()
        return Response({'is_bookmarked': False, 'bookmark_count': prompt.bookmarks.count()})
    return Response({'is_bookmarked': True, 'bookmark_count': prompt.bookmarks.count()})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_prompt(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    user_input = request.data.get('user_input')

    result = f"[GPT 응답 예시] Prompt: {prompt.content}, Input: {user_input}"

    execution = prompt.execution_set.create(
        user=request.user,
        user_input=user_input,
        result=result,
    )

    return Response({
        "prompt_id": prompt.id,
        "user_input": user_input,
        "result": result,
        "executed_at": execution.executed_at,
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, prompt_id):
    prompt = get_object_or_404(Prompt, id=prompt_id)

    if request.method == 'GET':
        comments = prompt.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, prompt=prompt)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return Response({'detail': '삭제 권한이 없습니다.'}, status=403)
    comment.delete()
    return Response(status=204)

# Toggle like on a comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    return Response({
        'likes': comment.likes.count(),
        'is_liked': comment.likes.filter(id=user.id).exists()
    })
