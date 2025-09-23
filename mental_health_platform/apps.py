from django.apps import AppConfig


class MentalHealthPlatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mental_health_platform'
    verbose_name = 'Mental Health Platform'

    def ready(self):
        # Import admin configuration when Django is ready
        try:
            from . import admin
        except ImportError:
            pass