from django.urls import path
from backend.views.viewsMain import *
from backend.views.viewsUser import *
from backend.views.viewsQuiz import *
from backend.views.viewsTeacher import *

urlpatterns = [

    path('quiz/<slug:slug>/edit/', editQuiz, name='quizEdit'),
    path('question/<slug:slug>/add/', QuestionAnswerCreate.as_view(), name='questionAdd'),
    path('questions/<int:pk>/', QuestionAnswerUpdate.as_view(), name='questionUpdate'),
    path('question/<int:pk>/', QuestionDelete.as_view(), name='questionDelete'),

    path('', index, name='homeView'),
    path('course/', CourseListView.as_view(), name='courseList'),
    path('course/add/', addCourse, name='addCourse'),
    path('course/subscribe/', CourseListSubscribeView.as_view(), name='courseListSubscribe'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='courseDetail'),
    path('course/<slug:slug>/edit', editCourse, name='editCourse'),
    path('course/<slug:slug>/delete', deleteCourse, name='deleteCourse'),
    path('course/<slug:slug>/subscribe', courseSubscribe, name='courseSubscribe'),
    path('course/<slug:slug>/unsubscribe', courseUnSubscribe, name='courseUnSubscribe'),

    path('section/<slug:slug>/edit/', editSection, name='sectionEdit'),
    path('section/<slug:slug>/delete/', deleteSection, name='sectionDelete'),
    path('section/<slug:slug>/add/', addSection, name='sectionAdd'),

    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='articleDetail'),
    path('article/<slug:slug>/add/', addArticle, name='addArticle'),
    path('article/<slug:slug>/edit/', editArticle, name='editArticle'),
    path('article/<slug:slug>/delete/', deleteArticle, name='deleteArticle'),

    path('task/<slug:slug>/add/', addAssignment, name='addAssignment'),
    path('task/<slug:slug>/edit/', editAssignment, name='editAssignment'),
    path('task/<slug:slug>/delete/', deleteAssignment, name='deleteAssignment'),
    path('task/<slug:slug>/', AssignmentDetailView.as_view(), name='taskDetail'),

    path('quiz/<slug:slug>/', quizView, name='quizDetail'),  # quizDetailView
    path('quiz/<slug:slug>/create/', createQuiz, name='createQuiz'),
    path('quiz/<slug:slug>/start/', QuizDetailView.as_view(), name='quizDetailView'),
    path('quiz/<slug:slug>/data/', quizDataView, name='quizDataDetail'),  # quizDataDetail
    path('quiz/<slug:slug>/save/', saveQuizView, name='saveQuizView'),

    path('teacher_course/', courseAssignmentView.as_view(), name='courseAssignmentView'),
    path('upload_task/<slug:slug>/', UploadAssignmentView.as_view(), name='UploadAnswerTaskView'),
    path('upload_tasks/<slug:slug>/', resultAssignmentList, name='resultUploadList'),

    path('profile/', profile, name='profile'),
    path('login/', loginStudent, name='loginStudent'),
    path('register/', registerStudent, name='registerStudent'),
    path('logout/', logoutStudent, name='logoutStudent'),
    path('profile/<slug:slug>/', StudentDetailView.as_view(), name='studentDetail'),

]
