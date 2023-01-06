from django.apps import AppConfig


class Rel8TenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Rel8Tenant'



    def ready(self) -> None:
        from . import signals
        return super().ready()