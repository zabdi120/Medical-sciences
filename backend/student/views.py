import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Max
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from accounts.permissions import IsTeacher, IsStudent

from .models import Student, Question, ExamResult, LearningContent
from .serializers import (
    QuestionSerializer, StudentSerializer,
    LearningContentSerializer, QuestionWriteSerializer,
    ExamResultDetailSerializer
)


class StudentLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        s_number = request.data.get('student_number')
        name = request.data.get('full_name')
        if not s_number or not name:
            return Response({"error": "student_number و full_name الزامی هستند"}, status=status.HTTP_400_BAD_REQUEST)
        student, created = Student.objects.get_or_create(
            student_number=s_number,
            defaults={'full_name': name}
        )
        refresh = RefreshToken()
        refresh['student_id'] = student.id
        refresh['student_number'] = student.student_number
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "student_id": student.id,
            "message": "خوش آمدید"
        }, status=status.HTTP_200_OK)


class GetRandomExamView(APIView):
    authentication_classes = []
    permission_classes = [IsStudent]

    def get(self, request):
        all_questions = list(Question.objects.all())
        count = min(len(all_questions), 20)
        random_questions = random.sample(all_questions, count)
        serializer = QuestionSerializer(random_questions, many=True)
        return Response(serializer.data)


class SubmitExamView(APIView):
    authentication_classes = []
    permission_classes = [IsStudent]

    def post(self, request):
        student_id = request.student_id
        user_answers = request.data.get('answers')
        if not user_answers:
            return Response({"error": "answers الزامی است"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "دانشجو یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        correct_answers_count = 0
        total = len(user_answers)
        for item in user_answers:
            try:
                question = Question.objects.get(id=item['question_id'])
                if question.correct_answer == item['selected_option']:
                    correct_answers_count += 1
            except Question.DoesNotExist:
                continue
        final_score = round((correct_answers_count / total) * 20, 2) if total > 0 else 0
        ExamResult.objects.create(student=student, score=final_score)
        return Response({
            "score": final_score,
            "correct": correct_answers_count,
            "total": total
        }, status=status.HTTP_201_CREATED)


class QuestionListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        questions = Question.objects.all()
        difficulty = request.query_params.get('difficulty')
        if difficulty in ['easy', 'medium', 'hard']:
            questions = questions.filter(difficulty=difficulty)
        serializer = QuestionWriteSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return None

    def get(self, request, pk):
        q = self.get_object(pk)
        if not q:
            return Response({"error": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        return Response(QuestionWriteSerializer(q).data)

    def put(self, request, pk):
        q = self.get_object(pk)
        if not q:
            return Response({"error": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionWriteSerializer(q, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        q = self.get_object(pk)
        if not q:
            return Response({"error": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        q.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LearningContentListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        contents = LearningContent.objects.all().order_by('-created_at')
        serializer = LearningContentSerializer(contents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LearningContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LearningContentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_object(self, pk):
        try:
            return LearningContent.objects.get(pk=pk)
        except LearningContent.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        return Response(LearningContentSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LearningContentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LearningContentPublicView(APIView):
    def get(self, request):
        contents = LearningContent.objects.all().order_by('-created_at')
        serializer = LearningContentSerializer(contents, many=True)
        return Response(serializer.data)


class TeacherStatsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        results = ExamResult.objects.select_related('student').all().order_by('-date_taken')
        total_exams = ExamResult.objects.count()
        avg_score = ExamResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
        max_score = ExamResult.objects.aggregate(mx=Max('score'))['mx'] or 0
        serializer = ExamResultDetailSerializer(results, many=True)
        return Response({
            "total_exams": total_exams,
            "average_score": round(avg_score, 2),
            "highest_score": max_score,
            "results": serializer.data
        })
