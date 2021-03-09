from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('course/', CourseListView.as_view(), name='courseList'),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='courseDetail'),
]
