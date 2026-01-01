from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Student, Question, ExamResult

admin.site.register(Student)
admin.site.register(Question)
admin.site.register(ExamResult)