from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Replace 'app' with your actual app name

    def ready(self):
        # Import your custom signal handlers
        import app.signals  # Replace 'app' with your actual app name