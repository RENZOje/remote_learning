from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from ..decorators import allowed_users
from ..forms import ResultUploadAnswerTaskForm
from ..models import *


def resultUploadList(request, slug):
    uploadAnswerTaskSet = UploadTask.objects.get(slug=slug).uploadanswertask_set.all()

    context = {'uploadAnswerTaskSet': uploadAnswerTaskSet}
    return render(request, 'screen/reviewUploadTask.html', context)


def reviewUploadTask(request, slug):
    form = ResultUploadAnswerTaskForm()

    context = {'form': form}
    return render(request, 'screen/reviewUploadTask.html', context)


class UploadAnswerTaskView(DetailView):
    model = UploadAnswerTask
    template_name = 'screen/taskUploadReview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.object.resultuploadanswertask)
        # print(dir(self.object))

        context['form'] = ResultUploadAnswerTaskForm(initial={'task': UploadAnswerTask.objects.get(id=self.object.id)})

        return context

    def post(self, request, *args, **kwargs):
        form = ResultUploadAnswerTaskForm(request.POST)
        if form.is_valid():
            uploadAnswer = UploadAnswerTask.objects.get(id=form.cleaned_data['task'].id)
            uploadAnswer.rated = True
            uploadAnswer.save()
            form.save()
            return redirect('/')
