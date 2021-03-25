from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UploadAssignment, Student, ResultAssignment


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
