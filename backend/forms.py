from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CreateStudentForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UploadAssignmentForm(forms.ModelForm):
    class Meta:
        model = UploadAssignment
        fields = ['comment', 'pdf_answer', 'studentUpload', 'answer']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'slug']


class ResultAssignmentForm(forms.ModelForm):
    class Meta:
        model = ResultAssignment
        fields = '__all__'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title','description']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        exclude = ['slug']