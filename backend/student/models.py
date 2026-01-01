from django.db import models
from accounts.models import models
# Create your models here.


class Student(models.Model):
    student_number = models.CharField(max_length=20, unique=True, verbose_name="شماره دانشجویی")
    full_name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")

    def __str__(self):
        return f"{self.full_name} ({self.student_number})"


class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="دانشجو")
    score = models.FloatField(verbose_name="نمره نهایی")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آزمون")

    def __str__(self):
        return f"{self.student.full_name} - نمره: {self.score}"
    

    from django.db import models


class Question(models.Model):
    text = models.TextField(verbose_name="متن سوال")
    option1 = models.CharField(max_length=200, verbose_name="گزینه ۱")
    option2 = models.CharField(max_length=200, verbose_name="گزینه ۲")
    option3 = models.CharField(max_length=200, verbose_name="گزینه ۳")
    option4 = models.CharField(max_length=200, verbose_name="گزینه ۴")
 
    correct_answer = models.IntegerField(verbose_name="شماره گزینه صحیح")

    def __str__(self):
        return self.text[:30]

    