from django.apps import AppConfig


class DueappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dueapp'


    def ready(self) -> None:
        from . import signal