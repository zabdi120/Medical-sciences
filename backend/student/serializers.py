from rest_framework import serializers
from .models import Student, Question, ExamResult, LearningContent

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_number', 'full_name', 'created_at']

class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.full_name')
    
    class Meta:
        model = ExamResult
        fields = ['id', 'student_name', 'score', 'date_taken']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'difficulty']


class LearningContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningContent
        fields = ['id', 'title', 'body', 'file', 'created_at', 'updated_at']

class QuestionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'difficulty', 'created_at']

class ExamResultDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.full_name')
    student_number = serializers.ReadOnlyField(source='student.student_number')

    class Meta:
        model = ExamResult
        fields = ['id', 'student_name', 'student_number', 'score', 'date_taken']
