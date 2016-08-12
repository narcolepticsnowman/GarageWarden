from django.apps import AppConfig
from GarageWarden import settings
import signal
from . import control
import RPi.GPIO as GPIO


class GarageControlConfig(AppConfig):
    name = 'garageControl'
    is_ready = False

    def ready(self):
        if not self.is_ready:
            self.is_ready = True
            GPIO.setwarnings(False)
            GPIO.cleanup()
            signal.signal(signal.SIGINT, cleanup_gpio)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(settings.GARAGE_RELAY_PIN, GPIO.OUT)
            GPIO.setup(settings.FULL_CLOSE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(settings.FULL_OPEN_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(settings.FULL_CLOSE_SWITCH_PIN, GPIO.RISING, callback=control.update_last_contact,
                                  bouncetime=200)
            GPIO.add_event_detect(settings.FULL_OPEN_SWITCH_PIN, GPIO.RISING, callback=control.update_last_contact,
                                  bouncetime=200)


def cleanup_gpio(signal, frame):
    GPIO.cleanup()
