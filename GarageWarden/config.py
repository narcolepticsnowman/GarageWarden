import RPi.GPIO as GPIO
from django.apps import AppConfig
from GarageWarden import settings
from threading import Timer


# use a dict to prevent duplicated callbacks
state_change_callbacks = {}


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
            GPIO.setup(settings.FULL_CLOSE_SWITCH_PIN, GPIO.IN)
            GPIO.setup(settings.FULL_OPEN_SWITCH_PIN, GPIO.IN)
            GPIO.setup(settings.BEEPER_PIN, GPIO.OUT)
            print("Adding callbacks for notification")
            # We detect both because we need to know both sides of state change
            GPIO.add_event_detect(settings.FULL_CLOSE_SWITCH_PIN, GPIO.BOTH, callback=self.callback,
                                  bouncetime=settings.SWITCH_PIN_DEBOUNCE_TIME)
            GPIO.add_event_detect(settings.FULL_OPEN_SWITCH_PIN, GPIO.BOTH, callback=self.callback,
                                  bouncetime=settings.SWITCH_PIN_DEBOUNCE_TIME)
            # import this here so django does't explode
            from GarageWarden.autoclose import state_change
            state_change_callbacks['autoclose'] = state_change
            print("Setup complete")

    def callback(self, channel):
        # This method effectively debounces the event detection so that the detecting methods can accurately check the
        # state of the switches
        print("Event detected for channel: " + str(channel) + ". Starting timers for listeners.")
        wait_time = settings.SWITCH_PIN_DEBOUNCE_TIME / 1000
        for m in state_change_callbacks.values():
            Timer(wait_time, m).start()
