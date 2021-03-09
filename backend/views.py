from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import *
from itertools import chain
from operator import attrgetter

# Create your views here.
def index(request):
    # course = Course.objects.all()[0]
    # section_one = course.section_set.all()[0]
    # list_work = sorted(chain(section_one.article_set.all(), section_one.quiz_set.all()), key=attrgetter('createdAt'))
    # for x in list_work:
    #     print(x.title, x.createdAt)

    return render(request, 'base.html')



class CourseListView(ListView):
    model = Course
    template_name = 'screen/courseListView.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'screen/courseDetailView.html'