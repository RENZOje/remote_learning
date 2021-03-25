from django.contrib import admin
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Teacher)
admin.site.register(Section)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Group_custom)
admin.site.register(UploadTask)
admin.site.register(UploadAnswerTask)

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(ResultQuiz)
admin.site.register(ResultUploadAnswerTask)


class AtricleAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = AtricleAdminForm

admin.site.register(Article, ArticleAdmin)