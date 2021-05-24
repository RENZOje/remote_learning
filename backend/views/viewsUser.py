from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from ..decorators import allowed_users
from ..forms import CreateStudentForm, StudentForm
from ..models import *


def profile(request):
    student = get_object_or_404(Student, id=request.user.student.id)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student, initial={'slug': student.slug})
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'screen/studentFormView.html', context)


class StudentDetailView(DetailView):
    model = Student
    template_name = 'screen/studentView.html'


def registerStudent(request):
    form = CreateStudentForm()
    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            Student.objects.create(user=user)
            messages.success(request, 'Account was created for ' + username)

            return redirect('loginStudent')

    context = {'form': form}
    return render(request, 'screen/register.html', context)


def loginStudent(request):
    if request.user.is_authenticated:
        return redirect('homeView')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homeView')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'screen/login.html', context)


def logoutStudent(request):
    logout(request)
    return redirect('homeView')
