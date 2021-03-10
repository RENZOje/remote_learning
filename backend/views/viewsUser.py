from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from ..decorators import allowed_users
from ..forms import CreateStudentForm
from ..models import *


@allowed_users(allowed_roles=['student'])
def profile(request):
    return render(request, 'screen/profileView.html')


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
                return redirect('mainView')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'screen/login.html', context)
