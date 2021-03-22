from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from backend.models import *
from ..forms import UploadAnswerTaskForm
from itertools import chain
from operator import attrgetter


# Create your views here.
def index(request):
    # course = Course.objects.all()[0]
    # section_one = course.section_set.all()[0]
    # print(dir(section_one))
    # list_work = sorted(chain(section_one.article_set.all(), section_one.quiz_set.all()), key=attrgetter('createdAt'))
    # for x in list_work:
    #     print(x.title, x.createdAt)

    return render(request, 'base.html')


class CourseListView(ListView):
    model = Course
    template_name = 'screen/courseListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'screen/courseDetailView.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'screen/taskDetailView.html'


def courseSubscribe(request, slug):
    student = request.user.student
    course = Course.objects.get(slug=slug)
    course.students.add(student)
    course.save()

    return redirect('courseList')


class TaskDetailView(DetailView):
    model = UploadTask
    template_name = 'screen/taskUploadDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_object = UploadAnswerTask.objects.filter(studentUpload_id=self.request.user.student.id).filter(
            answer__id=self.object.id)
        if len(query_object) != 0:
            context['answered'] = query_object[0]
            return context
        else:
            context['form'] = UploadAnswerTaskForm(
                initial={'studentUpload': Student.objects.get(id=self.request.user.student.id),
                         'answer': UploadTask.objects.get(id=self.object.id)})
            return context

    def post(self, request, *args, **kwargs):
        form = UploadAnswerTaskForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/')
