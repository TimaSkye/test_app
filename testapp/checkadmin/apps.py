from django.apps import AppConfig


class CheckadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkadmin'

    def ready(self):
        import checkadmin.signals