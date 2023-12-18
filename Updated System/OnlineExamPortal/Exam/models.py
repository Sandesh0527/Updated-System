from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Exam(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    duration = models.IntegerField()  # Duration in minutes
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey("Exam", on_delete=models.CASCADE)
    text = models.TextField()
    marks = models.DecimalField(max_digits=5, decimal_places=2)


class Choice(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey("Exam", on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    submission_time = models.DateTimeField(auto_now_add=True)
    exam_total = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.exam.name}"
