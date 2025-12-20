from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TeacherLoginSerializer, TeacherProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacher

#Teacher Login 
class TeacherLoginView(APIView):
    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "name": user.first_name
        })


#Teacher Profile
class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        serializer = TeacherProfileSerializer(request.user)
        return Response(serializer.data)