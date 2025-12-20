from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

#Teacher Login
class TeacherLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if not user or user.role != 'teacher':
            raise serializers.ValidationError("Invalid credentials")
        return user
