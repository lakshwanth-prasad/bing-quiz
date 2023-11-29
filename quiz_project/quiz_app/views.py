from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Quiz, Question, Result,Topic
from .forms import LoginForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Result
from django.contrib import messages
import random
def login_view(request):    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quiz_dashboard') 
            else:
                messages.error(request, 'Incorrect username or password')
        else:
            messages.error(request, 'Incorrect username or password Please Check the Credentials')
        return redirect('login_view')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

#Function to Select Quiz Topic Dashboard
def quiz_dashboard(request):
    topics = Topic.objects.all()
    return render(request, 'quiz_dashboard.html', {'topics': topics})

@login_required
def topic_quizzes(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    quizzes = topic.quizzes.all()
    return render(request, 'topic_quizzes.html', {'topic': topic, 'quizzes': quizzes})

@login_required
def quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())
    if len(questions) >=2:
        questions= random.sample(questions, 2)
    else:
        questions = []    
    return render(request, 'quiz_page.html', {'quiz': quiz, 'questions': questions})

#Function to Fetch the Questions and Quiz Details
def questions(request, topic_id):
    topic = Topic.objects.get(topic_id=topic_id)
    questions = topic.questions.all()   
    return render(request, 'quiz_page.html', {'questions': questions, 'topic': topic})

def quiz_result(request, quiz_id):
    # Assuming a Result model that stores user scores
    result = get_object_or_404(Result, quiz_id=quiz_id, user=request.user)
    return render(request, 'quiz_result.html', {'result': result})

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total_questions = quiz.questions.count()
    if request.method == 'POST':
        score = 0
        for question in quiz.questions.all():
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option and selected_option == question.correct_answer:
                score += 1
        percentage = (score / total_questions) * 100        
        Result.objects.create(user=request.user, quiz=quiz, score=score)
        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score,'percentage': percentage})
    else:
        return redirect('quiz_page', quiz_id=quiz_id)
    
def logout_view(request):
    logout(request)
    return redirect('login_view')  # Replace 'login_view' with the name of your login URL.


      

