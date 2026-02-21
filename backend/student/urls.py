from django.urls import path
from .views import (
    StudentLoginView,
    GetRandomExamView,
    SubmitExamView,
    QuestionListCreateView,
    QuestionDetailView,
    LearningContentListCreateView,
    LearningContentDetailView,
    LearningContentPublicView,
    TeacherStatsView,
)

urlpatterns = [
    # دانشجو
    path('student-login/', StudentLoginView.as_view(), name='student-login'),
    path('get-exam/', GetRandomExamView.as_view(), name='get-exam'),
    path('submit-exam/', SubmitExamView.as_view(), name='submit-exam'),
    path('contents/', LearningContentPublicView.as_view(), name='public-contents'),

    # استاد - سوالات
    path('teacher/questions/', QuestionListCreateView.as_view(), name='question-list'),
    path('teacher/questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),

    # استاد - محتوای درسی
    path('teacher/contents/', LearningContentListCreateView.as_view(), name='content-list'),
    path('teacher/contents/<int:pk>/', LearningContentDetailView.as_view(), name='content-detail'),

    # استاد - آمار
    path('teacher/stats/', TeacherStatsView.as_view(), name='teacher-stats'),
]
