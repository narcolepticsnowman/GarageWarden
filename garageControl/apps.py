from django.apps import AppConfig


class GarageControlConfig(AppConfig):
    name = 'garageControl'
    is_ready = False
    def ready(self):
        if not self.is_ready:
            is_ready = True
