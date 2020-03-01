from hashlib import blake2b

from django import forms
from django.forms import ValidationError
from django.core import signing
from django.core.mail import send_mail
from django.core.signing import Signer
from django.core.validators import RegexValidator

from pretalx.common.urls import build_absolute_uri


class SignupForm(forms.Form):
    email = forms.EmailField(required=True)

    def send_email(self, event):
        """Send the email once the form was validated.

        :param event: The current event is used as salt
        """
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

        # TODO vmx 2020-03-01: Make the email a proper template and use
        # pretalx code for it
        send_mail(
            "Community voting test",
            f"This is still in development, but please try voting at {vote_url}",
            "vmx7@uber.space",
            [self.cleaned_data["email"]],
            fail_silently=False,
        )


class ApiValidationFormGet(forms.Form):
    """This form is only used for validating GET parameters."""

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
    score = forms.IntegerField(required=False, min_value=0, max_value=2)
    user = forms.CharField(required=True)

    def __init__(self, event, data, **kwargs):
        """Custom constructor as we need the event for validation."""
        super(ApiValidationFormGet, self).__init__(data, **kwargs)
        self.event = event

    def clean_user(self):
        """Validate the signature of the user."""
        signed_user = self.cleaned_data["user"]

        # TODO vmx 2020-02-15: Move the email signing etc into its own class
        # so that it can be used from views and forms using the same signer
        signer = Signer(salt=self.event)
        try:
            user = signer.unsign(signed_user)
        except signing.BadSignature:
            # TODO vmx 2020-02-15: Use gettext for error message
            raise ValidationError("Invalid user")

        return user


class ApiValidationFormPost(ApiValidationFormGet):
    """This form is only used for validating POST parameters.

    It has the same constraints as for getting a value, the only difference
    is that you need to provide a score.
    """

    score = forms.IntegerField(required=True, min_value=0, max_value=2)
