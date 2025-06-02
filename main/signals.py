# apps.py
from django.apps import AppConfig

class mainonfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals  # 👈 Make sure signals are loaded
