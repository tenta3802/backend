from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from file.models import File
from file.serializers import UploadFileSerializer, GetFileSerializer
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from minio import Minio

import base64
from io import BytesIO

minio = Minio(
           '127.0.0.1:9000',
            access_key='tE2a63iV41ijm9u40DIW',
            secret_key='pCmcpUjSetGXwVIViWa4jftKG1n8jFzvnXjH8G6G',
            secure=False
        )

class UploadFile(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = UploadFileSerializer(data=request.data, context={'request': request})
    
        file_data = request.data.get('upload_file')
        if serializer.is_valid():
            serializer.save(file=file_data)

        file_content = file_data.read()
        file_stream = BytesIO(file_content)
        
        result = minio.put_object(
            "files",
            file_data.name,
            file_stream,
            len(file_content)
        )
        return Response(status=status.HTTP_200_OK)
    
class GetOriginFile(APIView):
    
    def get(self, request, file_id):
        file = get_object_or_404(File, id=file_id)
        serializer = GetFileSerializer(file)
        
        file_name = serializer.data.get('name')

        response = minio.get_object(
            'files',
            file_name
        )

        return Response(response, status=status.HTTP_200_OK)
