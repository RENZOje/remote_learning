from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from itertools import chain
from operator import attrgetter

# Create your models here.
class Group_custom(models.Model):
    name = models.CharField(max_length=10, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'Group: {self.name}'


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


class Course(models.Model):
    teachers = models.ManyToManyField(Teacher, blank=True)
    students = models.ManyToManyField(Student, blank=True)
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'Course: {self.title} Created: {self.teachers}'

    def get_absolute_url(self):
        return reverse('courseDetail', kwargs={'slug': self.slug})


class Section(models.Model):
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def return_article(self):
        list_item = sorted(chain(self.article_set.all(), self.quiz_set.all()),
                     key=attrgetter('createdAt'))
        return list_item

    def __str__(self):
        return f'Section: {self.title} Course: {self.course.title}'


class Quiz(models.Model):
    title = models.CharField(max_length=250, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Article(models.Model):
    title = models.CharField(max_length=250, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.title}'
