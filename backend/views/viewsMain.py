from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..filters import CourseFilter
from backend.models import *
from ..forms import UploadAssignmentForm, AssignmentForm


# Create your views here.
def index(request):
    return render(request, 'base.html')


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'screen/courseListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CourseFilter(self.request.GET, queryset=Course.objects.filter())
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'screen/courseDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.object.id)
        students = course.students.all()
        grade = [Grade.objects.get(student=student, course=course) for student in students]
        context['mainList'] = list(enumerate(zip(students, grade), 1))

        return context


class CourseListSubscribeView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'screen/courseListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CourseFilter(self.request.GET,
                                         queryset=Course.objects.filter(students__in=[self.request.user.student]))
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'screen/articleView.html'


def courseSubscribe(request, slug):
    student = request.user.student
    course = Course.objects.get(slug=slug)
    grade = Grade.objects.get_or_create(student=student, course=course)
    course.students.add(student)
    course.save()

    return redirect('courseList')


def courseUnSubscribe(request, slug):
    student = request.user.student
    course = Course.objects.get(slug=slug)
    course.students.remove(student)
    course.save()

    return redirect('courseList')


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'screen/assignmentDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_object = UploadAssignment.objects.filter(studentUpload_id=self.request.user.student.id).filter(
            answer__id=self.object.id)
        if len(query_object) != 0:
            context['answered'] = query_object[0]
            return context
        else:
            context['form'] = UploadAssignmentForm(
                initial={'studentUpload': Student.objects.get(id=self.request.user.student.id),
                         'answer': Assignment.objects.get(id=self.object.id)})
            return context

    def post(self, request, *args, **kwargs):
        form = UploadAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save()
            return redirect('UploadAnswerTaskView', slug=m.slug)


def addAssignment(request, slug):
    section = Section.objects.get(slug=slug)
    form = AssignmentForm(initial={"section": section})
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('courseDetail', slug=section.course.slug)

    context = {'form': form}
    return render(request, 'screen/addArticle.html', context=context)


def editAssignment(request, slug):
    assig = Assignment.objects.get(slug=slug)
    section = assig.section
    form = AssignmentForm(instance=assig, initial={"section": section})
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assig, initial={"section": section})
        if form.is_valid():
            form.save()
            return redirect('taskDetail', slug=assig.slug)

    context = {'form': form, 'object': assig}
    return render(request, 'screen/editArticle.html', context=context)


def deleteAssignment(request, slug):
    assig = Assignment.objects.get(slug=slug)
    course = assig.section.course
    if request.method == "GET":
        assig.delete()
        return redirect('courseDetail', slug=course.slug)
