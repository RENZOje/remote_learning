from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from ..forms import ResultAssignmentForm, SectionForm, CourseForm
from ..models import *


def addCourse(request):
    teacher = request.user.teacher
    form = CourseForm(initial={"teachers": teacher})
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courseList')

    context = {'form': form}
    return render(request, 'screen/addCourse.html', context=context)


def editCourse(request, slug):
    course = Course.objects.get(slug=slug)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()

    context = {'form': form, 'course': course}
    return render(request, 'screen/editCourse.html', context=context)

def deleteCourse(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "GET":
        course.delete()
        return redirect('courseList')

def addSection(request, slug):
    course = Course.objects.get(slug=slug)
    form = SectionForm(initial={"course":course})
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courseDetail', slug=course.slug)

    context = {'form': form, 'course': course}
    return render(request, 'screen/addSection.html', context=context)


def editSection(request, slug):
    section = Section.objects.get(slug=slug)
    form = SectionForm(instance=section)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()

    context = {'form': form, 'object': section}
    return render(request, 'screen/editSection.html', context=context)


def deleteSection(request, slug):
    section = Section.objects.get(slug=slug)
    course = section.course
    if request.method == "GET":
        section.delete()
        return redirect('courseDetail', slug=course.slug)


def resultAssignmentList(request, slug):
    uploadassignmentSet = list(enumerate(Assignment.objects.get(slug=slug).uploadassignment_set.all(), 1))

    context = {'uploadAssignmentSet': uploadassignmentSet}
    return render(request, 'screen/resultAssignmentList.html', context)


class UploadAssignmentView(DetailView):
    model = UploadAssignment
    template_name = 'screen/assignmentReview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResultAssignmentForm(initial={'task': UploadAssignment.objects.get(id=self.object.id)})
        return context

    def post(self, request, *args, **kwargs):
        form = ResultAssignmentForm(request.POST)

        if form.is_valid():
            uploadAnswer = UploadAssignment.objects.get(id=form.cleaned_data['task'].id)
            uploadAnswer.rated = True
            uploadAnswer.save()
            form.save()

            course = uploadAnswer.answer.section.course
            grade = Grade.objects.get(course=course, student=form.cleaned_data['task'].studentUpload)
            grade.amountPoint = float(round(grade.amountPoint, 2)) + float(round(form.cleaned_data['score'], 2))
            grade.save()

            return redirect('/')


class courseAssignmentView(ListView):
    model = Course
    template_name = 'screen/courseAssignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.filter(teachers=self.request.user.teacher)

        return context
