from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
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
        fields = ['title', 'description', 'draft', 'teachers', 'coursePicture']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        exclude = ['slug']


from django.forms import inlineformset_factory


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ()


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ()


QuestionFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=3)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'


class ArticleForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['slug']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ['slug']