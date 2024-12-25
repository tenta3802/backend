from rest_framework import serializers

from django.db import models
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = ('user_id', 'password')

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        filds = '__all__'