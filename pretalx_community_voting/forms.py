from hashlib import blake2b

from django import forms
from django.core.signing import Signer
from django.core.validators import RegexValidator

from pretalx.common.urls import build_absolute_uri


class SignupForm(forms.Form):
    email = forms.EmailField(required=True)

    def send_email(self, event):
        """Send the email once the form was validated.

        :param event: The current event is used as salt
        """
        print(f'sending the email to {self.cleaned_data["email"]}')

        # Use the hashed email as identifier for the votes
        email_hashed = blake2b(
            self.cleaned_data["email"].encode("utf-8"),
            salt=event.slug.encode("utf-8"),
            digest_size=16,
        ).hexdigest()

        # For the email link, sign the hashed email address, so that no one
        # can just randomly create new URLs and pretend to be a user that
        # was validated via email
        signer = Signer(salt=event.slug)
        email_signed = signer.sign(email_hashed)

        vote_url = build_absolute_uri(
            "plugins:pretalx_community_voting:talks",
            kwargs={"event": event.slug, "signed_user": email_signed},
        )
        print(f"vote_url: {vote_url}")


class ApiValidationForm(forms.Form):
    """This form is only used for validating POST parameters."""

    submission = forms.CharField(
        required=True,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^[0-9a-zA-Z]*$",
                message="Submission code may only contain alphanumeric characters.",
            )
        ],
    )
    score = forms.IntegerField(required=True, min_value=0, max_value=2)
    # TODO vmx 2020-02-09 add proper validator for signed username
    user = forms.CharField(required=True)
