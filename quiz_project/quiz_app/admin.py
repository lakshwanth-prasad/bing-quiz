from django.contrib import admin
from .models import Quiz, Question, Topic, Result

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Result)

