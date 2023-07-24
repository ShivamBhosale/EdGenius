from django.apps import AppConfig


class EdgeniusappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "EdGeniusApp"
    #
    # def ready(self):
    #     import EdGeniusApp.models