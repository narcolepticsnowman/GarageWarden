import RPi.GPIO as GPIO
from django.apps import AppConfig
from GarageWarden import settings, notify, autoclose
from threading import Timer


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
            # We detect both because we need to know both sides of state change
            GPIO.add_event_detect(settings.FULL_CLOSE_SWITCH_PIN, GPIO.BOTH, callback=self.callback,
                                  bouncetime=settings.SWITCH_PIN_DEBOUNCE_TIME)
            GPIO.add_event_detect(settings.FULL_OPEN_SWITCH_PIN, GPIO.BOTH, callback=self.callback,
                                  bouncetime=settings.SWITCH_PIN_DEBOUNCE_TIME)
            print("Setup complete")

    def callback(self, channel):
        # This method effectively debounces the event detection so that the detecting methods can accurately check the
        # state of the switches
        print("Event detected for channel: " + str(channel) + ". Starting timers for listeners.")
        wait_time = settings.SWITCH_PIN_DEBOUNCE_TIME / 1000
        Timer(wait_time, notify.state_change).start()
        Timer(wait_time, autoclose.state_change).start()
