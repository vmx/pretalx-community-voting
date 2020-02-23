from django.conf.urls import url

from pretalx.event.models.event import SLUG_CHARS

from . import views

urlpatterns = [
    url(
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/signup/$",
        views.SignupView.as_view(),
        name="signup",
    ),
    url(
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/thanks/$",
        views.ThanksView.as_view(),
        name="thanks",
    ),
    url(
        # The user needs to be the last element of the URL due to the JS code
        # Trailing slashes are ignored by the JS code.
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/talks/(?P<signed_user>[^/]+)/$",
        views.SubmissionListView.as_view(),
        name="talks",
    ),
    url(
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/api/$",
        views.ApiView.as_view(),
        name="api",
    ),
]
