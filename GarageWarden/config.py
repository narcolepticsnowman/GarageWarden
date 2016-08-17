import RPi.GPIO as GPIO
import signal

from django.apps import AppConfig

from GarageWarden import settings, control


class Config(AppConfig):
    name = 'GarageWarden'
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
            GPIO.add_event_detect(settings.FULL_CLOSE_SWITCH_PIN, GPIO.BOTH, callback=control.update_last_contact,
                                  bouncetime=200)
            GPIO.add_event_detect(settings.FULL_OPEN_SWITCH_PIN, GPIO.BOTH, callback=control.update_last_contact,
                                  bouncetime=200)


def cleanup_gpio(signal, frame):
    GPIO.cleanup()
