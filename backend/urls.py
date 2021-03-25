from django.urls import path
from backend.views.viewsMain import *
from backend.views.viewsUser import *
from backend.views.viewsQuiz import *
from backend.views.viewsTeacher import *

urlpatterns = [
    path('', index, name='homeView'),
    path('course/', CourseListView.as_view(), name='courseList'),
    path('course/subscribe/', CourseListSubscribeView.as_view(), name='courseListSubscribe'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='courseDetail'),
    path('course/<slug:slug>/subscribe', courseSubscribe, name='courseSubscribe'),
    path('course/<slug:slug>/unsubscribe', courseUnSubscribe, name='courseUnSubscribe'),

    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='articleDetail'),
    path('task/<slug:slug>/', AssignmentDetailView.as_view(), name='taskDetail'),

    path('quiz/<slug:slug>/start/', QuizDetailView.as_view(), name='quizDetailView'),
    path('quiz/<slug:slug>/', quizView, name='quizDetail'),  # quizDetailView
    path('quiz/<slug:slug>/data/', quizDataView, name='quizDataDetail'),  # quizDataDetail
    path('quiz/<slug:slug>/save/', saveQuizView, name='saveQuizView'),

    path('upload_task/<slug:slug>/', UploadAssignmentView.as_view(), name='UploadAnswerTaskView'),
    path('upload_tasks/<slug:slug>/', resultAssignmentList, name='resultUploadList'),

    path('profile/', profile, name='profile'),
    path('login/', loginStudent, name='loginStudent'),
    path('register/', registerStudent, name='registerStudent'),
    path('logout/', logoutStudent, name='logoutStudent'),
    path('profile/<slug:slug>/', StudentDetailView.as_view(), name='studentDetail'),

]
