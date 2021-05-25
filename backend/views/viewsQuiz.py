from django.db import transaction
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, DeleteView, ListView, UpdateView
from ..models import *
from ..forms import *

from ..forms import QuestionFormSet


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
        grade.amountPoint = float(round(grade.amountPoint, 2)) + float(round(score_, 2))
        grade.save()

        if score_ >= quiz.required_score_to_pass:
            context = {'passed': True, 'score': round(score_, 2), 'results': results}
            return JsonResponse(context)
        else:
            context = {'passed': False, 'score': round(score_, 2), 'results': results}
            return JsonResponse(context)


def createQuiz(request, slug):
    section = Section.objects.get(slug=slug)
    form = QuizForm(initial={"section": section})
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sectionEdit', slug=section.slug)

    context = {'form': form, 'section': section}
    return render(request, 'quiz/createQuiz.html', context=context)


def editQuiz(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    questions = quiz.question_set.all()

    context = {'questions': questions, 'quiz': quiz}
    return render(request, 'quiz/question_list.html', context=context)


class QuestionCreate(CreateView):
    model = Question
    fields = ['text', 'quiz']


class QuestionAnswerCreate(CreateView):
    model = Question
    fields = ['text', 'quiz']
    template_name = 'quiz/question_form.html'

    def get_success_url(self):
        quiz = self.object.quiz.slug
        return reverse_lazy('quizEdit',kwargs={'slug': quiz},)

    def get_initial(self):
        quiz = get_object_or_404(Quiz, slug=self.kwargs.get('slug'))
        return {
            'quiz':quiz,
        }

    def get_context_data(self, **kwargs):
        data = super(QuestionAnswerCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['questionQuizList'] = QuestionFormSet(self.request.POST, )
        else:
            data['questionQuizList'] = QuestionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(self.object)
        familymembers = context['questionQuizList']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(QuestionAnswerCreate, self).form_valid(form)


class QuestionUpdate(UpdateView):
    model = Question
    success_url = '/'
    fields = ['text', 'quiz']


class QuestionAnswerUpdate(UpdateView):
    model = Question
    fields = ['text', 'quiz']
    template_name = 'quiz/question_form.html'

    def get_success_url(self):
        quiz = self.object.quiz.slug
        return reverse_lazy('quizEdit',kwargs={'slug': quiz},)

    def get_context_data(self, **kwargs):
        data = super(QuestionAnswerUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['questionQuizList'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            data['questionQuizList'] = QuestionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questionQuizList = context['questionQuizList']
        with transaction.atomic():
            self.object = form.save()

            if questionQuizList.is_valid():
                questionQuizList.instance = self.object
                questionQuizList.save()
        return super(QuestionAnswerUpdate, self).form_valid(form)


class QuestionDelete(DeleteView):
    model = Question
    template_name = 'quiz/question_confirm_delete.html'

    def get_success_url(self):
        quiz = self.object.quiz.slug
        return reverse_lazy('quizEdit',kwargs={'slug': quiz},)
