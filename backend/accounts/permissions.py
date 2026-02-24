from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return False
        token_str = auth_header.split(' ')[1]
        try:
            token = AccessToken(token_str)
            student_id = token.get('student_id')
            if not student_id:
                return False
            request.student_id = student_id
            return True
        except Exception:
            return False
