from django.shortcuts import render
from django.views.generic import ListView
from .models import *


# Create your views here.
class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/main.html'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    context = {'obj': quiz}

    return render(request, 'quiz/quiz.html', context)
