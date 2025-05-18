from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from .models import Like, Bookmark
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Prompt, Execution, Comment
from .serializers import PromptSerializer, ExecutionSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Prompt.objects.all()
        if self.request.query_params.get('mine') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        if self.request.query_params.get('liked') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(likes__user=self.request.user)
        if self.request.query_params.get('bookmarked') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(bookmarks__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExecutionViewSet(viewsets.ModelViewSet):
    queryset = Execution.objects.order_by('-executed_at')
    serializer_class = ExecutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Execution.objects.filter(user=self.request.user)


# CommentViewSet 추가
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToggleLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        prompt = Prompt.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, prompt=prompt)

        if not created:
            like.delete()
            return Response({"liked": False, "like_count": prompt.likes.count()})
        else:
            return Response({"liked": True, "like_count": prompt.likes.count()})


class ToggleBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        prompt = Prompt.objects.get(pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, prompt=prompt)

        if not created:
            bookmark.delete()
            return Response({"bookmarked": False, "bookmark_count": prompt.bookmarks.count()})
        else:
            return Response({"bookmarked": True, "bookmark_count": prompt.bookmarks.count()})


# ExecutePromptView 추가
class ExecutePromptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        prompt = get_object_or_404(Prompt, pk=pk)
        user_input = request.data.get('user_input')

        # GPT 호출 더미 응답
        result = f"[GPT 응답 예시] Prompt: {prompt.content}, Input: {user_input}"

        execution = Execution.objects.create(
            prompt=prompt,
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
