from django.apps import AppConfig


class LiveTrackingDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'live_tracking_data'
class LiveTrackingDataConfig(AppConfig):
    name = 'live_tracking_data'

    def ready(self):
        import live_tracking_data.signals  # Ensure the signals are imported