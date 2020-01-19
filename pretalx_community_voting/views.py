from django.views.generic.list import ListView

from pretalx.submission.models import Submission


class SubmissionListView(ListView):
    model = Submission
