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
    try:
        result = ResultQuiz.objects.get(quiz=quiz, student=request.user.student)
        context = {'object': quiz, 'resultQuiz': result}
        return render(request, 'quiz/quiz.html', context)
    except:
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


def saveQuizView(request, slug):
    print(request.POST)
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        student = request.user.student
        quiz = Quiz.objects.get(slug=slug)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correctAnswer = None

        for q in questions:
            answerSelected = request.POST.get(str(q.text))
            if answerSelected != '':
                questionAnswer = Answer.objects.filter(question=q)
                for a in questionAnswer:
                    if answerSelected == a.text:
                        if a.correct:
                            score += 1
                            correctAnswer = a.text
                    else:
                        if a.correct:
                            correctAnswer = a.text
                results.append({str(q): {'correctAnswer': correctAnswer}, 'answered': answerSelected})

            else:
                results.append({str(q): 'Not answered'})
        score_ = score * multiplier
        ResultQuiz.objects.create(quiz=quiz, student=student, score=score_)

        course = quiz.section.course
        grade = Grade.objects.get(course=course, student=student)
        grade.amountPoint = int(grade.amountPoint) + int(score_)
        grade.save()

        if score_ >= quiz.required_score_to_pass:
            context = {'passed': True, 'score': round(score_, 2), 'results': results}
            return JsonResponse(context)
        else:
            context = {'passed': False, 'score': round(score_, 2), 'results': results}
            return JsonResponse(context)
