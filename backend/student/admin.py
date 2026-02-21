from django.contrib import admin
from django.contrib import admin
from .models import Student, Question, ExamResult, LearningContent

admin.site.register(Student)
admin.site.register(Question)
admin.site.register(ExamResult)
admin.site.register(LearningContent)