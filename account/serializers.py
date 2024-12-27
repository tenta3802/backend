from rest_framework import serializers

from django.db import models
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source="group.name")
    class Meta:
        model = User
        fields = ('id', 'password', 'group_name', 'user_id', 'user_name', 'is_active', 'is_admin', 'is_staff', 'is_superuser')
        extra_kwargs = {"password": {"write_only": True}}

class UserCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'password', 'is_staff')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserPasswordChangeSerializer(serializers.ModelSerializer):
    current = serializers.CharField(write_only=True)
    target = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current', 'target')
        extra_kwargs = {
            'current': {'write_only': True},
            'target': {'write_only': True},
        }
    
    def validate_current(self, current):
        user = self.context['request'].user
        if not user.check_password(current):
            raise serializers.ValidationError("Current password is not matched")
        return current