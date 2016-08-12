from django.http import JsonResponse
from django.views import View
import RPi.GPIO as GPIO
from GarageWarden import settings

class StatusView(View):
    def get(self, request):
        return JsonResponse({"garageFullOpen":garage_is_full_open(), "garageFullClose":garage_is_full_close()})


def garage_is_full_open():
    return GPIO.input(settings.FULL_OPEN_SWITCH_PIN)


def garage_is_full_close():
    return GPIO.input(settings.FULL_CLOSE_SWITCH_PIN)
