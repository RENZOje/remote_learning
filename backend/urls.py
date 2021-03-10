from django.urls import path
from backend.views.viewsMain import *
from backend.views.viewsUser import *

urlpatterns = [
    path('', index, name='homeView'),
    path('course/', CourseListView.as_view(), name='courseList'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='courseDetail'),

    path('profile/', profile, name='profile'),
    path('login/', loginStudent, name='loginStudent'),
    path('register/', registerStudent, name='registerStudent'),
]
