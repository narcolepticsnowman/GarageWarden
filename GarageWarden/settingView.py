from django.views.generic import View
from django.http import JsonResponse
import json
from GarageWarden.models import Setting
from GarageWarden import login
from django.forms.models import model_to_dict


reload_methods = {}


class SettingView(login.AuthorizedMixin, View):
    def post(self, request):
        if request.body is None or len(request.body) < 1:
            return self.make_bad_request("A request body is required")
        body = json.loads(request.body.decode('utf-8'))
        if "key" not in body or "value" not in body:
            return self.make_bad_request("Key or Value missing from request")
        setting = Setting.objects.filter(key=body["key"])[:1]
        if not setting.exists():
            return self.make_bad_request("Unknown setting")
        setting = setting.get()
        if setting.type == "B" and body["value"] not in ["True", "False"]:
            return self.make_bad_request("Value for boolean setting must be True or False")
        if setting.type == "N" and not body["value"].replace(".", "", 1).isDigit():
            return self.make_bad_request("Value for number setting must be a valid number")
        setting.value = body['value']
        setting.save()
        for m in reload_methods:
            m()
        return JsonResponse(model_to_dict(setting))

    def get(self, request):
        if 'key' in request.GET:
            return JsonResponse(model_to_dict(Setting.objects.get(key=request.GET['key'])))
        return JsonResponse({k['key']: k for k in list(Setting.objects.order_by("key").values())})
