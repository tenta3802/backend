from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import timedelta

from account.models import User
from account.models import Group
from account.serializers import UserSerializer, UserCreateSerialize, UserPasswordChangeSerializer


class UserList(APIView):
    
    def get(self, request):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        serializers = UserCreateSerialize(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_404_NOT_FOUND)
    
class UserDetail(APIView):

    def get_object(self, user_id):
        return get_object_or_404(User, user_id=user_id)

    def get(self, request, user_id):
        user = self.get_object(user_id=user_id)
        serializers = UserSerializer(user)
        return Response(serializers.data)
    
    # put, delete는 로그인 기능 구현 후 테스트
    def put(self, request, user_id):
        serializer = UserPasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = self.get_object(user_id=user_id)
            user.set_password(request.data.get('target'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        if request.user.is_admin:
            user = self.get_object(user_id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        if not user_id or not password:
            return Response({"detail": "user_id and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Does Not Exist User"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"detail": "Invalid Password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timedelta(minutes=15))
        refresh.set_exp(lifetime=timedelta(days=7))

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
    
class UserJoinGruiop(APIView):

    def put(self, request):
        login_user = request.user
        login_user_group = get_object_or_404(Group, id=login_user.group_id)
        queryset = User.objects.filter(user_id=request.data.get('user_id'))

        if login_user.is_admin:
            queryset.update(group=login_user_group)
        else:
            group = get_object_or_404(Group, name=request.data.get('group_name'))
            if login_user.group_id != group.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            queryset.update(group=group)
        return Response(status=status.HTTP_200_OK)
        