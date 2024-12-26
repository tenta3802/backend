from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Crypto.Cipher import AES

from account.models import User
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