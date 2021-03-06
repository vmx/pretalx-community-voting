import random

from django.core import signing
from django.core.signing import Signer
from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from pretalx.submission.models import Submission

from .forms import SignupForm, ApiValidationFormGet, ApiValidationFormPost
from .models import Vote


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

    # If the user is unvalid, it will stay "None"
    user = None

    def get_queryset(self):
        # TODO vmx 2020-02-02: Move the email signing etc into its own class
        # so that it can be used from views and forms using the same signer
        signer = Signer(salt=self.kwargs["event"])
        try:
            self.user = signer.unsign(self.kwargs["signed_user"])
        except signing.BadSignature:
            self.user = None
            # If the use wasn't valid, there is no point of returning a
            # QuerySet with the talks
            return None

        votes = Vote.objects.filter(
            user=self.user, submission_id=OuterRef("pk")
        ).values("score")
        submissions = list(
            Submission.objects.all().annotate(score=Subquery(votes))
        )
        random.seed(self.user)
        random.shuffle(submissions)
        return submissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context


class ApiView(View):
    # TODO vmx 2020-02-15: Unify this code with the one from the POST request
    def get(self, request, event):
        vote_data = ApiValidationFormGet(event, request.GET)
        if not vote_data.is_valid():
            return JsonResponse({"error": "Invalid data."}, status=500)

        try:
            submission = Submission.objects.get(
                event=request.event, code=vote_data.cleaned_data["submission"]
            )
        except Submission.DoesNotExist:
            return JsonResponse(
                {
                    "error": "Submission not found.",
                    "submission": vote_data.cleaned_data["submission"],
                },
                status=404,
            )
        try:
            vote = Vote.objects.get(
                user=vote_data.cleaned_data["user"], submission=submission
            )
        except Vote.DoesNotExist:
            return JsonResponse({"error": "Not voted yet."}, status=404)

        response = {"score": vote.score, "submission": vote.submission.code}
        return JsonResponse(response)

    def post(self, request, event):
        vote_data = ApiValidationFormPost(event, request.POST)
        if not vote_data.is_valid():
            # TODO vmx 2020-02-15: Return better error messages
            return JsonResponse({"error": "Invalid data."}, status=500)

        try:
            submission = Submission.objects.get(
                event=request.event, code=vote_data.cleaned_data["submission"]
            )
        except Submission.DoesNotExist:
            return JsonResponse(
                {
                    "error": "Submission not found.",
                    "submission": vote_data.cleaned_data["submission"],
                },
                status=404,
            )
        try:
            # Update any existing vote
            vote = Vote.objects.get(
                user=vote_data.cleaned_data["user"], submission=submission
            )
            vote.score = vote_data.cleaned_data["score"]
        except Vote.DoesNotExist:
            # If the user hasn't voted yet, create a new vote
            vote = Vote(
                score=vote_data.cleaned_data["score"],
                user=vote_data.cleaned_data["user"],
                submission=submission,
            )
        vote.save()

        response = {"score": vote.score, "submission": vote.submission.code}
        return JsonResponse(response)
