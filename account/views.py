from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from account.serializers import UserSerializer


class UserList(APIView):
    
    def get(self):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_404_NOT_FOUND)
    
class UserDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, pk):
        user = self.get_object(pk=pk)
        serializers = UserSerializer(user)
        return Response(serializers.data)
    
    def put(self, request, pk):
        user = self.get_object(pk=pk)
        serializers = UserSerializer(user)
        new_password = request.GET.get('targetPassword')

        if serializers.is_valid():
            serializers.set_password(new_password)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializers.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, pk):
        user = self.get_object(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
