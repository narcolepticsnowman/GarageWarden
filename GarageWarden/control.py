import RPi.GPIO as GPIO
import json
import time
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from GarageWarden import settings, status, login

# init this to now minus the needed time so the requests work as soon as the system starts up
last_request = datetime.now() - timedelta(seconds=settings.REQUEST_DEBOUNCE)


class ControlView(login.AuthorizedMixin, View):
    def post(self, request):
        global last_request
        if request.body is None or len(request.body) < 1:
            return self.make_bad_request("A request body is required")
        data = json.loads(request.body.decode('utf-8'))
        if 'open' not in data:
            return self.make_bad_request("You must specify whether the door should be open or not")

        should_be_open = data['open']
        if not isinstance(should_be_open, bool):
            return self.make_bad_request("The \"open\" property can only be True or False")

        is_full_open = status.garage_is_full_open()
        is_full_closed = status.garage_is_full_close()
        request_time = datetime.now()

        time_since_last_request = (request_time - last_request).total_seconds()
        if time_since_last_request < settings.REQUEST_DEBOUNCE:
            return HttpResponse("Too many request, try again in a few seconds", status=503)
        changed = False
        if should_be_open and not is_full_open or not should_be_open and not is_full_closed:
            trigger_door()
            last_request = request_time
            changed = True
        return JsonResponse({"changed": changed})


def trigger_door():
    # close the relay temporarily then re-open it to trigger the door to close
    GPIO.output(settings.GARAGE_RELAY_PIN, True)
    time.sleep(settings.GARAGE_RELAY_TRIGGER_LENGTH)
    GPIO.output(settings.GARAGE_RELAY_PIN, False)
    pass
