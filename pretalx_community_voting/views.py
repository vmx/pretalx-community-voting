import random

from django.core import signing
from django.core.signing import Signer
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
        form.send_email(self.request.event)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO vmx 2020-02-02: Move the email signing etc into its own class
        # so that it can be used from views and forms using the same signer
        signer = Signer(salt=self.kwargs["event"])
        try:
            user = signer.unsign(self.kwargs["signed_user"])
            context["user"] = user
            context["valid_user"] = True
        except signing.BadSignature:
            context["valid_user"] = False

        return context
