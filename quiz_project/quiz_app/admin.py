from django.contrib import admin
from .models import Quiz, Question, Topic, Result, Student
from .views import *

# TO REGISTER OUR DATABASE MODELS FOR CRUD OPERATIONS
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Result)
admin.site.register(Student)

