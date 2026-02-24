from django.db import models

class Student(models.Model):
    student_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_number})"


class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="دانشجو")
    score = models.FloatField(verbose_name="نمره نهایی")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آزمون")

    def __str__(self):
        return f"{self.student.full_name} - نمره: {self.score}"


class Question(models.Model):
    text = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=1)
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy', 'آسان'), ('medium', 'متوسط'), ('hard', 'سخت')],
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text[:50]

class LearningContent(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    file = models.FileField(upload_to='learning_content_files/', null=True, blank=True)  # ← اضافه کن
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
