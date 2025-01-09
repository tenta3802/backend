from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from datetime import timedelta

from account.models import User
from account.models import Group
from account.schemas import *
from account.serializers import(UserSerializer,
                                UserCreateSerialize,
                                UserPasswordChangeSerializer,
)

class UserList(APIView):
    
    @extend_schema(
        tags=["account"],
        summary="Get User List API",
        description="user 전체 목록 반환<br>"
    )
    def get(self, request, *args, **kwargs):
        users = User.objects.all().select_related('group')
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    
    @extend_schema(
        tags=["account"],
        summary="Register User API",
        description="user 생성<br>"
    )
    def post(self, request, *args, **kwargs):
        serializers = UserCreateSerialize(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class UserDetail(APIView):

    def get_object(self, user_id):
        return get_object_or_404(User, user_id=user_id)

    @extend_schema(
        tags=["account"],
        summary="Get User Info API",
        description="user 정보 반환<br>"
    )
    def get(self, request, user_id):
        user = self.get_object(user_id=user_id)
        serializers = UserSerializer(user)
        return Response(serializers.data)
    
    @extend_schema(
        tags=["account"],
        summary="Delete User Info API",
        description="user 정보 삭제<br>"
    )
    def delete(self, request, user_id):
        if request.user.is_admin:
            user = self.get_object(user_id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["account"],
        summary="Issue Token API",
        description="user_id, password를 받아 access, refresh token 반환<br>",
        request=USER_SIGNIN_REQUEST,
        responses=USER_SIGNIN_RESPONSES,
        examples=USER_SIGNIN_EXAMPLES,
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        if not user_id or not password:
            return Response({"message": "user_id and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_id=user_id)
            user.count = 0
        except User.DoesNotExist:
            return Response({"message": "Does Not Exist User"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"message": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timedelta(minutes=300))
        refresh.set_exp(lifetime=timedelta(days=7))

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
    
class UserJoinGruiop(APIView):

    @extend_schema(
        tags=["account"],
        summary="Join User In Group API",
        description="user group에 포함 시키는 API<br>"
    )
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
    
class UserActivate(APIView):

    @extend_schema(
        tags=["account"],
        summary="Active User API",
        description="user 활성화 API<br>"
    )
    def put(self, request):
        try:
            user = User.objects.get(user_name=request.data.get('user_name'))
        except User.DoesNotExist:
            return Response({"detail": "Does Not Exist User"}, status=status.HTTP_401_UNAUTHORIZED)        
        if user.is_active == 0:
            user.is_active = 1 
        user.save()
        return Response(status=status.HTTP_200_OK)
        
class UserName(APIView):

    @extend_schema(
        tags=["account"],
        summary="Change User Name API",
        description="user 이름 변경 API<br>"
    )
    def put(self, request):
        current_name = request.user.user_name
        target_name = request.data.get('user_name')
        
        try:
            user = User.objects.get(user_name=current_name)
        except User.DoesNotExist:
            return Response({"detail": "Does Not Exist User"}, status=status.HTTP_401_UNAUTHORIZED)        
        
        users = User.objects.filter(user_name=target_name)
        if users:
            return Response({"detail": "Already Exist User Name"}, status=status.HTTP_400_BAD_REQUEST)        

        if current_name != target_name:
            user.user_name = target_name
            user.save()
        return Response(status=status.HTTP_200_OK)                 

class UserPassword(APIView):

    @extend_schema(
        tags=["account"],
        summary="Change Password API",
        description="user 비밀번호 변경 API<br>"
    )
    def put(self, request):
        serializer = UserPasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User.objects.get(user_id=request.user.user_id)
            user.set_password(request.data.get('target'))
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)     
    
class UserCount(APIView):

    @extend_schema(
        tags=["account"],
        summary="Plus User Password Fail Count",
        description="user 비밀번호 실패 횟수 업데이트 API<br>"
    )
    def put(self, request):
        try:
            user = User.objects.get(user_id=request.data.get('user_id'))
        except User.DoesNotExist:
            return Response({"detail": "Does Not Exist User"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_admin:
            if user.count < 5:
                user.count += 1
            if user.count == 5:
                user.is_active = False
            user.save()
        return Response(status=status.HTTP_200_OK)