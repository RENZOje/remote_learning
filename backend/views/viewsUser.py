from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..forms import CreateStudentForm
from ..models import *


def profile(request):
    return render(request, 'screen/profileView.html')


def registerStudent(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateStudentForm()
        if request.method == 'POST':
            form = CreateStudentForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('loginStudent')

        context = {'form': form}
    return render(request, 'screen/register.html', context)


def loginStudent(request):
    if request.user.is_authenticated:
        return redirect('home')
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
