from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
import json


class LoginView(View):
    def post(self, request):
        if request.body is None or len(request.body) < 1:
            return HttpResponse("A request body is required", status=400)

        data = json.loads(request.body.decode('utf-8'))

        if 'username' not in data or not data['username']:
            return self.make_bad_request("Username is required.")
        if 'password' not in data or not data['password']:
            return self.make_bad_request("Password is required.")

        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"loggedIn": True, "name": self.get_name(user)})
        else:
            return HttpResponse("Invalid username or password.", status=401)

    def get(self, request):
        return JsonResponse({"loggedIn": request.user.is_authenticated(), "name": self.get_name(request.user)})

    def get_name(self, user):
        if user.is_anonymous():
            return "anonymous"
        return user.first_name if user.first_name else user.username

    def make_bad_request(self, error):
        return HttpResponse(error, status=400)


class AuthorizedMixin:
    """
    CBV mixin which verifies that the current user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Not logged in", status=401)
        return super(AuthorizedMixin, self).dispatch(request, *args, **kwargs)

    def make_bad_request(self, error):
        return HttpResponse(error, status=400)
