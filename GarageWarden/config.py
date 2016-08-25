import RPi.GPIO as GPIO
from django.apps import AppConfig
from GarageWarden import settings, notify, autoclose

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
            # For notification, we only want to detect falling edges since that tells us that the switch just closed
            # This means we can know how to notify simply by inspecting the channel the event happened on
            GPIO.add_event_detect(settings.FULL_CLOSE_SWITCH_PIN, GPIO.FALLING, callback=notify.switch_closed_notify,
                                  bouncetime=settings.SWITCH_PIN_DEBOUNCE_TIME)
            GPIO.add_event_detect(settings.FULL_OPEN_SWITCH_PIN, GPIO.FALLING, callback=notify.switch_closed_notify,
                                  bouncetime=settings.SWITCH_PIN_DEBOUNCE_TIME)
            print("Setup complete")
