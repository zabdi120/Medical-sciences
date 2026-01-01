from django.shortcuts import render

# Create your views here.
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Question, ExamResult
from .serializers import QuestionSerializer, StudentSerializer

class StudentLoginView(APIView):
    def post(self, request):
        s_number = request.data.get('student_number')
        name = request.data.get('full_name')
        
  
        student, created = Student.objects.get_or_create(
            student_number=s_number, 
            defaults={'full_name': name}
        )
        return Response({"student_id": student.id, "message": "خوش آمدید"}, status=status.HTTP_200_OK)


class GetRandomExamView(APIView):
    def get(self, request):
       
        all_questions = list(Question.objects.all())
        
   
        count = min(len(all_questions), 20)
        
  
        random_questions = random.sample(all_questions, count)
        
    
        serializer = QuestionSerializer(random_questions, many=True)
        return Response(serializer.data)


class SubmitExamView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        user_answers = request.data.get('answers') 
        
        correct_answers_count = 0
        
        for item in user_answers:
            question = Question.objects.get(id=item['question_id'])
            if question.correct_answer == item['selected_option']:
                correct_answers_count += 1
        
       
        final_score = (correct_answers_count / 20) * 20
        
        
        student = Student.objects.get(id=student_id)
        ExamResult.objects.create(student=student, score=final_score)
        
        return Response({"score": final_score}, status=status.HTTP_201_CREATED)