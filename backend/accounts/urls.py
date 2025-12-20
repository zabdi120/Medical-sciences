from django.urls import path
from .views import TeacherLoginView, TeacherProfileView

urlpatterns = [
    path('teacher/login/', TeacherLoginView.as_view()),
    path('teacher/profile/', TeacherProfileView.as_view()),
]
