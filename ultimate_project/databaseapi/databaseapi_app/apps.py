from django.apps import AppConfig


class DatabaseApiAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "databaseapi_app"

    def ready(self):
        import databaseapi_app.signals