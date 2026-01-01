from rest_framework import serializers
from .models import Student, ExamResult, Question 

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_number', 'full_name']

class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.full_name')
    
    class Meta:
        model = ExamResult
        fields = ['id', 'student_name', 'score', 'date_taken']



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
       
        fields = ['id', 'text', 'option1', 'option2', 'option3', 'option4']
