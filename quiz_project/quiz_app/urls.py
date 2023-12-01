from django.urls import path
from django.contrib import admin
from . import views

# CHANGING THE ADMIN SITES NAME
admin.site.site_header = 'Bing Quiz Admin'

# GENERATING URL PATTERNS FOR NAVIGATION OF PAGES
urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('quiz_dashboard/', views.quiz_dashboard, name='quiz_dashboard'),
    path('topics/<int:topic_id>/', views.topic_quizzes, name='topic_quizzes'),    
    path('quiz/<int:quiz_id>/', views.quiz_page, name='quiz_page'),
    path('submit_quiz/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('admin_login_view/', views.admin_login_view, name='admin_login_view'),
    path('visualize_results/', views.visualize_results, name='visualize_results'),
    path('logout/', views.logout_view, name='logout_view'),
    # Admin URLs...
]
