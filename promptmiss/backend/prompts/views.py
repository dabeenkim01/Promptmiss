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
from rest_framework.generics import UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        print("🔍 요청 유저:", user)
        queryset = Prompt.objects.all()

        try:
            if self.request.query_params.get('mine') == 'true':
                if user.is_authenticated:
                    print("📌 mine 필터 활성화")
                    queryset = queryset.filter(user=user)
            elif self.request.query_params.get('liked') == 'true':
                if user.is_authenticated:
                    print("📌 liked 필터 활성화")
                    queryset = queryset.filter(prompt_likes__user=user)
            elif self.request.query_params.get('bookmarked') == 'true':
                if user.is_authenticated:
                    print("📌 bookmarked 필터 활성화")
                    queryset = queryset.filter(bookmarks__user=user)
        except Exception as e:
            print("❌ get_queryset 오류 발생:", e)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mine(self, request):
        # /api/prompts/mine/ 엔드포인트 추가
        prompts = Prompt.objects.filter(user=request.user)
        serializer = self.get_serializer(prompts, many=True)
        return Response(serializer.data)
    

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
            return Response({"is_liked": False, "like_count": prompt.prompt_likes.count()})
        else:
            return Response({"is_liked": True, "like_count": prompt.prompt_likes.count()})


class ToggleBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        prompt = Prompt.objects.get(pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, prompt=prompt)

        if not created:
            bookmark.delete()
            return Response({"is_bookmarked": False, "bookmark_count": prompt.bookmarks.count()})
        else:
            return Response({"is_bookmarked": True, "bookmark_count": prompt.bookmarks.count()})


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


class PromptUpdateView(UpdateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise PermissionDenied("수정 권한이 없습니다.")
        serializer.save()


class PromptListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mine = request.query_params.get('mine', None)
        if mine == 'true':
            prompts = Prompt.objects.filter(user=request.user)  # 현재 사용자만 필터링
        else:
            prompts = Prompt.objects.all()
        serializer = PromptSerializer(prompts, many=True)
        return Response(serializer.data)
