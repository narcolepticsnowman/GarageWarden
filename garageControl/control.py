from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import json
from . import status
from GarageWarden import settings
import RPi.GPIO as GPIO
import time

# init this to now minus the needed time so the requests work as soon as the system starts up
last_contact = datetime.now() - timedelta(seconds=settings.MIN_TIME_BETWEEN_REQUESTS)


@method_decorator(csrf_exempt, name='dispatch')
class ControlView(View):
    def post(self, request):
        if request.body is None or len(request.body) < 1:
            return HttpResponse("A request body is required", status=400)
        data = json.loads(request.body.decode('utf-8'))
        if 'open' not in data:
            return self.make_bad_request("You must specify whether the door should be open or not")

        should_be_open = data['open']
        if not isinstance(should_be_open, bool):
            return self.make_bad_request("The \"open\" property can only be True or False")

        is_full_closed = status.garage_is_full_open()
        is_full_open = status.garage_is_full_close()
        request_time = datetime.now()
        elapsed = (request_time - last_contact).total_seconds()
        if not is_full_open and not is_full_closed and elapsed < settings.MIN_TIME_BETWEEN_REQUESTS:
            return HttpResponse("Door is currently operating. Please try again later", status=503)

        changed = False
        if should_be_open and not is_full_open or not should_be_open and not is_full_closed:
            trigger_door()
            changed = True
        return JsonResponse({"changed": changed})

    def make_bad_request(self, error):
        return HttpResponse(error, status=400)


def trigger_door():
    # close the relay temporarily then re-open it to trigger the door to close
    GPIO.output(settings.GARAGE_RELAY_PIN, True)
    time.sleep(settings.GARAGE_RELAY_TRIGGER_LENGTH)
    GPIO.output(settings.GARAGE_RELAY_PIN, False)
    pass


def update_last_contact(channel):
    global last_contact
    last_contact = datetime.now()
    print("updated last contact to:"+last_contact.strftime("%d-%b-%Y %H:%M:%S"))
