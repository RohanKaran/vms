from django.apps import AppConfig


# noinspection PyUnresolvedReferences
class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        import api.purchase_orders.signals
        import api.users.signals
