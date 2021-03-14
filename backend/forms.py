from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UploadAnswerTask, Student


class CreateStudentForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


from django import forms



class UploadAnswerTaskForm(forms.ModelForm):
	class Meta:
		model = UploadAnswerTask
		fields = ['comment','pdf_answer']



class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		exclude = ['user','slug']