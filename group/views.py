from os import name
import stat
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from group.models import Group
from group.serializers import GroupSerializer

class GroupList(APIView):

    def get(self, request):
        groups = Group.objects.all()
        serializers = GroupSerializer(groups, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        user = request.user
        serializers = GroupSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_404_NOT_FOUND)
    
class GroupDetail(APIView):
    
    def delete(self, request, name):
        if request.user.is_admin:
            group = get_object_or_404(Group, name=name)
            group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


