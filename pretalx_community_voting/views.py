import random

from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from pretalx.submission.models import Submission

from .forms import SignupForm


class SignupView(FormView):
    template_name = "submission/signup.html"
    form_class = SignupForm

    def get_success_url(self):
        return reverse(
            "plugins:pretalx_community_voting:thanks", kwargs=self.kwargs
        )

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ThanksView(TemplateView):
    template_name = "submission/thanks.html"


class SubmissionListView(ListView):
    model = Submission
    template_name = "submission/submission_list.html"

    def get_queryset(self):
        submissions = list(Submission.objects.all())
        random.seed("abcd")
        random.shuffle(submissions)
        return submissions
