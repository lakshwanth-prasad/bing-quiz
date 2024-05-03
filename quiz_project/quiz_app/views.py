from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Quiz, Question, Result,Topic,Student
from .forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Result
from django.contrib import messages
import random
from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Avg

# FUNCTION WILL HANDLE THE AUTHENTICATION OF STUDENT
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

# FUNCTION TO SELECT QUIZ DASHBOARD BASED ON TOPIC/COURSE ASSIGNMENT
def quiz_dashboard(request):
    if request.user.is_authenticated:
        assigned_topics = Topic.objects.filter(assigned_users=request.user)
    else:
        assigned_topics = []
    return render(request, 'quiz_dashboard.html', {'topics': assigned_topics})

# FUNCTION TO DISPLAY THE QUIZZES UNDER SPECIFIC TOPIC
@login_required
def topic_quizzes(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    quizzes = topic.quizzes.all()
    return render(request, 'topic_quizzes.html', {'topic': topic, 'quizzes': quizzes})

# FUNCTION TO DISPLAY THE QUIZ WITH TIMER AND LOGIC OF LESS THAN 10 QUESTION DONT DISPLAY THE QUIZ AND RANDOMIZE 5 QUESTIONS
@login_required
def quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())
    if len(questions) >=1:
        questions= random.sample(questions, 5)
    else:
        questions = []    
    return render(request, 'quiz_page.html', {'quiz': quiz, 'questions': questions})

# FUNCTION TO FETCH QUIZ DETAILS AND QUIZ ID
def questions(request, topic_id):
    topic = Topic.objects.get(topic_id=topic_id)
    questions = topic.questions.all()   
    return render(request, 'quiz_page.html', {'questions': questions, 'topic': topic})

# FUNCTION TO DISPLAY QUIZ RESULTS IN TOTAL MARKS AND PERCENTAGE
def quiz_result(request, quiz_id):
    result = get_object_or_404(Result, quiz_id=quiz_id, user=request.user)
    return render(request, 'quiz_result.html', {'result': result})

#FUNCTION TO HANDLE THE MATH FOR CALCULATING MARKS AND PERCENTAGE
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

#FUNCTION TO HANDLE ADMIN AUTHENTICATION    
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('visualize_results')
            else:
                messages.error(request, 'Not an admin or incorrect credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

#FUNCTION TO VISUALIZE RESULTS
def visualize_results(request):
    quizzes = Quiz.objects.all()
    selected_quiz_id = request.GET.get('quiz_id')
    graph_urls = []

    if selected_quiz_id:
        selected_quiz_id = int(selected_quiz_id)

        top_5_results = Result.objects.filter(quiz_id=selected_quiz_id).order_by('-score')[:5]
        bottom_5_results = Result.objects.filter(quiz_id=selected_quiz_id).order_by('score')[:5]
        average_score = Result.objects.filter(quiz_id=selected_quiz_id).aggregate(Avg('score'))['score__avg']
        average_score = average_score if average_score is not None else 0

        # Create separate figures for each graph
        for data, title, color in [
            (top_5_results, 'Top 5 Scores', 'green'),
            (bottom_5_results, 'Bottom 5 Scores', 'red'),
            ([average_score], 'Average Score', 'blue')
        ]:
            fig, ax = plt.subplots()
            scores = [result.score for result in data] if data != [average_score] else data
            users = [result.user.username for result in data] if data != [average_score] else ['Average']
            ax.bar(users, scores, color=color)
            ax.set_title(title)
            ax.set_ylabel('Scores')

            # Save and encode each figure
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graph = base64.b64encode(image_png)
            graph = graph.decode('utf-8')
            graph_urls.append(f"data:image/png;base64,{graph}")

            plt.close(fig)  # Close the figure

    return render(request, 'visualization.html', {
        'quizzes': quizzes,
        'graph_urls': graph_urls
    })
    
#FUNCTION TO HANDLE LOGOUT REQUESTS
def logout_view(request):
    logout(request)
    return redirect('login_view')  # Replace 'login_view' with the name of your login URL.


