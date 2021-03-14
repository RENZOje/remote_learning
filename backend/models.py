from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import unique_slugify
from itertools import chain
from operator import attrgetter
from django.core.validators import FileExtensionValidator


# Create your models here.
class Group_custom(models.Model):
    name = models.CharField(max_length=10, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}'


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=True)
    middleName = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'Teacher: {self.firstName} {self.lastName}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=True)
    middleName = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    about = models.CharField(max_length=250, blank=True)
    telegram_link = models.CharField(max_length=100, blank=True)
    group = models.ForeignKey(Group_custom, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'Student: {self.firstName} {self.lastName} Group: '

    def get_absolute_url(self):
        return reverse('studentDetail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((unique_slugify(self.firstName), unique_slugify(self.lastName)))
        super(Student, self).save(*args, **kwargs)


class Course(models.Model):
    teachers = models.ManyToManyField(Teacher, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f'Course: {self.title} Created: {self.teachers}'

    def get_absolute_url(self):
        return reverse('courseDetail', kwargs={'slug': self.slug})


class Section(models.Model):
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def return_article(self):
        list_item = sorted(chain(self.uploadtask_set.all(), self.article_set.all(), self.quiz_set.all()),
                           key=attrgetter('createdAt'))
        return list_item

    def __str__(self):
        return f'Section: {self.title} Course: {self.course.title}'


class Quiz(models.Model):
    title = models.CharField(max_length=250, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(Quiz, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('quizDetail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class Article(models.Model):
    title = models.CharField(max_length=250, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    description = models.TextField(default='')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articleDetail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class UploadTask(models.Model):
    title = models.CharField(max_length=250, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    description = models.TextField(default='')
    slug = models.SlugField(blank=True)
    pdf_task = models.FileField(upload_to='foo/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(UploadTask, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('taskDetail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class UploadAnswerTask(models.Model):
    answer = models.ForeignKey(UploadTask, on_delete=models.CASCADE, blank=True)
    studentUpload = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(default='', blank=True)
    pdf_answer = models.FileField(upload_to='pdfAnswer/',
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

