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
        f"^(?P<event>[{SLUG_CHARS}]+)/p/voting/vote/(?P<signed_user>[^/]+)/$",
        views.SubmissionListView.as_view(),
        name="vote",
    ),
]
