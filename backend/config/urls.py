from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
]
from django.urls import path
from student.views import StudentLoginView, GetRandomExamView, SubmitExamView

urlpatterns = [
    path('student-login/', StudentLoginView.as_view(), name='student_login'),
    path('get-exam/', GetRandomExamView.as_view(), name='get_exam'),
    path('submit-exam/', SubmitExamView.as_view(), name='submit_exam'),
]