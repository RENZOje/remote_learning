from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import unique_slugify
from itertools import chain
from operator import attrgetter
from django.core.validators import FileExtensionValidator
import random

# Create your models here.
class Group_custom(models.Model):
    name = models.CharField(max_length=10, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        if not self.slug:
            self.slug = unique_slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        teachers = ' '.join([f'Teacher {x.firstName} {x.lastName}' for x in self.teachers.all()])
        return f'Course: {self.title} Created: {teachers}'

    def get_absolute_url(self):
        return reverse('courseDetail', kwargs={'slug': self.slug})


class Section(models.Model):
    title = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField()

    def return_all_task(self):
        list_item = sorted(chain(self.assignment_set.all(), self.article_set.all(), self.quiz_set.all()),
                           key=attrgetter('createdAt'))
        return list_item

    def return_mark_task(self):
        list_item = sorted(chain(self.assignment_set.all(), self.quiz_set.all()),
                           key=attrgetter('createdAt'))
        return list_item

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self.title)
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return f'Section: {self.title} Course: {self.course.title}'


class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amountPoint = models.FloatField(default=0)


class Quiz(models.Model):
    title = models.CharField(max_length=250, blank=True)
    point = models.IntegerField(blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    createdAt = models.DateTimeField(auto_now_add=True)
    required_score_to_pass = models.IntegerField(help_text="required score in %")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(Quiz, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('quizDetailView', kwargs={'slug': self.slug})

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class ResultQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    score = models.FloatField()

    def __str__(self):
        return f'Quiz: {self.quiz}, student - {self.student.firstName}'

    # def quizPassed(self, request):
    #     if ResultQuiz.objects.get(quiz=self.quiz, student=request.user.student):
    #         return True
    #     else:
    #         return False

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


class Assignment(models.Model):
    title = models.CharField(max_length=250, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    description = models.TextField(default='')
    slug = models.SlugField(blank=True)
    pdf_task = models.FileField(upload_to='foo/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(Assignment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('taskDetail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class UploadAssignment(models.Model):
    answer = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True)
    studentUpload = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(default='', blank=True)
    pdf_answer = models.FileField(upload_to='pdfAnswer/',
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    slug = models.SlugField(blank=True,null=True)
    rated = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('UploadAnswerTaskView', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = '-'.join((unique_slugify(self.studentUpload.firstName), unique_slugify(self.answer.title)))
        super(UploadAssignment, self).save(*args, **kwargs)

    def __str__(self):
        return f'UploadAnswerTask: {self.answer.title}, student - {self.studentUpload.firstName}'


class ResultAssignment(models.Model):
    task = models.OneToOneField(UploadAssignment, on_delete=models.CASCADE)
    comment = models.TextField(blank=True,null=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f'Quiz: {self.task}, student - {self.task.studentUpload.firstName}'