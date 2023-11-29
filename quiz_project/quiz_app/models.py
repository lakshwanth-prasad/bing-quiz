from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=100)
    topic_id = models.IntegerField(max_length=100,default=1)
    def __str__(self):
        return self.name   

class Quiz(models.Model):
    title = models.CharField(max_length=200,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    quiz_id = models.IntegerField(unique=True ,max_length=100, default=1)
    description = models.TextField(null=True, blank=True)  # Allows for a longer text field for the description
    time_allowed = models.IntegerField(default=10)
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='questions')
    text = models.CharField(max_length=300)
    option1 = models.CharField(max_length=100,null=True)
    option2 = models.CharField(max_length=100,null=True)
    option3 = models.CharField(max_length=100,null=True)
    option4 = models.CharField(max_length=100,null=True)
    correct_answer = models.CharField(max_length=100,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    percentage = models.FloatField(null=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - {self.score}'
