from django.views.generic import View
from django.http import JsonResponse, HttpResponse
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
        settings_to_save = []
        try:
            if isinstance(body, list):
                for setting in body:
                    settings_to_save.append(self.validate_setting(setting))
            else:
                settings_to_save.append(self.validate_setting(body))
        except AssertionError as e:
            return self.make_bad_request(str(e))
        for s in settings_to_save:
            s.save()
        for m in reload_methods.values():
            m()
        return HttpResponse(None)

    def get(self, request):
        if 'key' in request.GET:
            return JsonResponse(model_to_dict(Setting.objects.get(key=request.GET['key'])))
        return JsonResponse({"settings": list(Setting.objects.order_by("order").values())})

    def validate_setting(self, input):
        if "key" not in input or "value" not in input:
            raise AssertionError("Key or Value missing from setting")
        setting = Setting.objects.filter(key=input["key"])[:1]
        if not setting.exists():
            raise AssertionError("Unknown setting: "+input["key"])
        setting = setting.get()
        if setting.type == "B" and input["value"] not in ["True", "False"]:
            raise AssertionError("Value for boolean setting must be True or False for key:"+setting.key)
        if setting.type == "N" and not input["value"].replace(".", "", 1).isDigit():
            return self.make_bad_request("Value for number setting must be a valid number for key:"+setting.key)
        setting.value = input['value']
        return setting
