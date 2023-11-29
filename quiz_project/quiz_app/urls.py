from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('quiz_dashboard/', views.quiz_dashboard, name='quiz_dashboard'),
    path('topics/<int:topic_id>/', views.topic_quizzes, name='topic_quizzes'),    
    path('quiz/<int:quiz_id>/', views.quiz_page, name='quiz_page'),
    path('submit_quiz/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('logout/', views.logout_view, name='logout_view'),
    # Admin URLs...
]
