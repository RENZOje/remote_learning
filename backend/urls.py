from django.urls import path
from backend.views.viewsMain import *
from backend.views.viewsUser import *
from backend.views.viewsQuiz import *

urlpatterns = [
    path('', index, name='homeView'),
    path('course/', CourseListView.as_view(), name='courseList'),
    path('course/subscribe/', CourseListSubscribeView.as_view(), name='courseListSubscribe'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='courseDetail'),
    path('course/<slug:slug>/subscribe', courseSubscribe, name='courseSubscribe'),

    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='articleDetail'),
    # path('quiz/<slug:slug>/', QuizDetailView.as_view(), name='quizDetail'),
    path('task/<slug:slug>/', TaskDetailView.as_view(), name='taskDetail'),

    path('quiz/<slug:slug>/start/', QuizDetailView.as_view(), name='quizDetailView'),
    path('quiz/<slug:slug>/', quizView, name='quizDetail'),  # quizDetailView
    path('quiz/<slug:slug>/data/', quizDataView, name='quizDataDetail'),  # quizDataDetail
    path('quiz/<slug:slug>/save/', saveQuizView, name='saveQuizView'),

    path('profile/', profile, name='profile'),
    path('login/', loginStudent, name='loginStudent'),
    path('register/', registerStudent, name='registerStudent'),
    path('logout/', logoutStudent, name='logoutStudent'),
    path('profile/<slug:slug>/', StudentDetailView.as_view(), name='studentDetail'),

]
