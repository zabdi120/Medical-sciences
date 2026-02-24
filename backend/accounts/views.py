from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TeacherLoginSerializer, TeacherProfileSerializer
from django.contrib.auth import authenticate
from .models import User
from .permissions import IsTeacher

#Teacher Login 
class TeacherLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role != 'teacher':
            return Response({'error': 'Not a teacher account'}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'username': user.username,
                'first_name': user.first_name,
                'role': user.role,
            }
        })


#Teacher Profile
class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        serializer = TeacherProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        data = request.data

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'username' in data:
            user.username = data['username']
        
        if 'password' in data:
            old_password = data.get('old_password')
            if not old_password:
                return Response({'error': 'old_password required'}, status=400)
            if not user.check_password(old_password):
                return Response({'error': 'Wrong current password'}, status=400)
            user.set_password(data['password'])
        
        user.save()
        return Response({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
