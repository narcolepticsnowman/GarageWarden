from django.http import JsonResponse
from django.views import View


class StatusView(View):
    def get(self, request):
        return JsonResponse({"garageOpen": self.garage_is_open()})

    def garage_is_open(self):
        return True
