import RPi.GPIO as GPIO
from django.apps import AppConfig
from GarageWarden import settings, notify


class Config(AppConfig):
    name = 'GarageWarden'
    is_ready = False

    def ready(self):
        if not self.is_ready:
            self.is_ready = True
            print("Setting up GPIO")
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(settings.GARAGE_RELAY_PIN, GPIO.OUT)
            GPIO.setup(settings.FULL_CLOSE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(settings.FULL_OPEN_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print("Adding callbacks for notification")
            GPIO.add_event_detect(settings.FULL_CLOSE_SWITCH_PIN, GPIO.BOTH, callback=notify.state_change_notify,
                                  bouncetime=200)
            GPIO.add_event_detect(settings.FULL_OPEN_SWITCH_PIN, GPIO.BOTH, callback=notify.state_change_notify,
                                  bouncetime=200)
            print("Setup complete")
