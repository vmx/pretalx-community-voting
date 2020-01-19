from django.conf.urls import url

from pretalx.event.models.event import SLUG_CHARS

from . import views

urlpatterns = [
    url(f'^(?P<event>[{SLUG_CHARS}]+)/p/voting/',
        views.SubmissionListView.as_view(), name='index'),
]
