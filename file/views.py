from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from file.models import File
from file.serializers import UploadFileSerializer, GetFileSerializer
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.temp import NamedTemporaryFile
from django.http import FileResponse

from minio import Minio
from pathlib import Path

import json
import base64
from io import BytesIO
minio = Minio(
           '127.0.0.1:9000',
            access_key='fs439xn8i6K9ayY83p4E',
            secret_key='lOqT7PVXt9rTJgDEEeRmuk6C33BcECaW4KEApcVw',
            secure=False
        )

class UploadFile(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = UploadFileSerializer(data=request.data, context={'request': request})
    
        file_data: TemporaryUploadedFile = request.data.get('upload_file')
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

    def post(self, request):
        file = get_object_or_404(File, id=request.data.get('file_id'))
        file_name = file.name
        file_type = Path(file_name).suffix
        content_type = 'application/java-archive' if file_type == '.jar' else None
        
        f = NamedTemporaryFile(mode="w+b")
        try:
            minio_file = minio.fget_object('files', file_name, f.name)        
        except minio.error.S3Error as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = FileResponse(open(f.name, "rb"), content_type=content_type)
        response["Content-Disposition"] = "inline; filename=" + file_name
        return response

class UploadDumpFile(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file: TemporaryUploadedFile = request.data.get('upload_file')
        result = minio.fput_object(
            "dump-files",
            request.data.get('file_id'),
            file.temporary_file_path()
        )
        return Response(status=status.HTTP_200_OK, data={'name':file.name})
    
class GetDumpFile(APIView):

    def post(self, request):
        file_id = str(request.data.get('file_id'))
        f = NamedTemporaryFile(mode="w+b")
        try:
            minio_file = minio.fget_object('dump-files', file_id, f.name)        
        except minio.error.S3Error as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=str(e))
        response = FileResponse(open(f.name, "rb"), content_type='application/zip')
        response["Content-Disposition"] = "inline; filename=" + file_id + '.zip'
        return response