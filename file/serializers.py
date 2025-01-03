from rest_framework import serializers
from file.models import File

class UploadFileSerializer(serializers.Serializer):
    upload_file = serializers.FileField(write_only=True)

    class Meta:
        model = File
        fields = ['upload_file']

    def save(self, file):
        name = file.name
        if not name.endswith('jar'):
            raise serializers.ValidationError('파일 확장자가 일치하지 않습니다.')
    
        user = self.context['request'].user
        file = File.objects.create(
            name = name,
            type = 'unit',
            group = user.group
        )
        return file
    
class GetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name')