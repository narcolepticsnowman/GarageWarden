from django.http import JsonResponse, HttpResponse
from django.views.generic import View
import RPi.GPIO as GPIO
from GarageWarden import settings


class StatusView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in", status=401)
        return JsonResponse({"garageFullOpen": garage_is_full_open(), "garageFullClose": garage_is_full_close()})


def garage_is_full_open():
    return 1 == GPIO.input(settings.FULL_OPEN_SWITCH_PIN)


def garage_is_full_close():
    return 1 == GPIO.input(settings.FULL_CLOSE_SWITCH_PIN)
