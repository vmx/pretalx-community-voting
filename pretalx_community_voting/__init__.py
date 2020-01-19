from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class PluginApp(AppConfig):
    name = "pretalx_community_voting"
    verbose_name = "pretalx community voting plugin"

    class PretalxPluginMeta:
        name = gettext_lazy("pretalx community voting plugin")
        author = "Volker Mische"
        description = gettext_lazy("A community voting plugin for pretalx")
        visible = True
        version = "0.1.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretalx_community_voting.PluginApp"
