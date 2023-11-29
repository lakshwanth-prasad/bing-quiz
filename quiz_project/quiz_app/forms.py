from django import forms
from django.contrib.auth.models import User
from .models import Quiz, Question,Result
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import transaction

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'topic']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_answer']