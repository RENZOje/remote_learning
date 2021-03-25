from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from ..forms import ResultAssignmentForm
from ..models import *


def resultAssignmentList(request, slug):
    uploadassignmentSet = Assignment.objects.get(slug=slug).uploadassignment_set.all()

    context = {'uploadAssignmentSet': uploadassignmentSet}
    return render(request, 'screen/resultAssignmentList.html', context)



class UploadAssignmentView(DetailView):
    model = UploadAssignment
    template_name = 'screen/assignmentReview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ResultAssignmentForm(initial={'task': UploadAssignment.objects.get(id=self.object.id)})

        return context

    def post(self, request, *args, **kwargs):
        form = ResultAssignmentForm(request.POST)
        if form.is_valid():
            uploadAnswer = UploadAssignment.objects.get(id=form.cleaned_data['task'].id)
            uploadAnswer.rated = True
            uploadAnswer.save()
            form.save()
            return redirect('/')
