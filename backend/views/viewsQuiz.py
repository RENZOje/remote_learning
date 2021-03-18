from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from ..models import *


# Create your views here.
# class QuizListView(ListView):
#     model = Quiz
#     template_name = 'quiz/main.html'


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/main.html'


def quizView(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    context = {'object': quiz}

    return render(request, 'quiz/quiz.html', context)


def quizDataView(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    context = {'data': questions,
               'time': quiz.time}

    return JsonResponse(context)
