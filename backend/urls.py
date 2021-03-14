from django.urls import path
from backend.views.viewsMain import *
from backend.views.viewsUser import *

urlpatterns = [
    path('', index, name='homeView'),
    path('course/', CourseListView.as_view(), name='courseList'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='courseDetail'),

    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='articleDetail'),
    path('quiz/<slug:slug>/', QuizDetailView.as_view(), name='quizDetail'),
    path('task/<slug:slug>/', TaskDetailView.as_view(), name='taskDetail'),

    path('profile/', profile, name='profile'),
    path('login/', loginStudent, name='loginStudent'),
    path('register/', registerStudent, name='registerStudent'),
    path('profile/<slug:slug>/', StudentDetailView.as_view(), name='studentDetail'),

]
