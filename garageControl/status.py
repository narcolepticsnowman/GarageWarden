from django.http import JsonResponse
from django.views import View


class StatusView(View):
    def get(self, request):
        return JsonResponse({"garageFullOpen":garage_is_full_open(), "garageFullClose":garage_is_full_close()})


def garage_is_full_open():
    return True


def garage_is_full_close():
    return False
