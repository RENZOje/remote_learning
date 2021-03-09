from django.urls import path
from .views import *

urlpatterns = [
    path('', QuizListView.as_view(), name='mainView'),
    path('<pk>/', quiz_view, name='quizView'),
]
