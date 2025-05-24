from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer, UserSerializer

User = get_user_model()

@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=404)

    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)