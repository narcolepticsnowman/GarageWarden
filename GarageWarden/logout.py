from django.views.generic import View
from django.contrib.auth import logout
from django.http import JsonResponse


class LogOutView(View):

    def get(self, request):
        logout(request)
        return JsonResponse({"loggedIn": False})
