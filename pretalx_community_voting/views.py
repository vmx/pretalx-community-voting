import random

from django.views.generic.list import ListView

from pretalx.submission.models import Submission


class SubmissionListView(ListView):
    model = Submission
    template_name = 'submission/submission_list.html'

    def get_queryset(self):
        submissions = list(Submission.objects.all())
        random.seed('abcd')
        random.shuffle(submissions)
        return submissions
