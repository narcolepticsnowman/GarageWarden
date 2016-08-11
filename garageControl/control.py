from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import json
from . import status

min_time_between_requests = 120
last_contact = datetime.now()


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

        if not is_full_open and not is_full_closed:
            return HttpResponse("Door is currently operating. Please try again later", status=503)

        changed=False
        if should_be_open and is_full_closed or not should_be_open and is_full_open:
            # trigger_door
            changed=True
        return JsonResponse({"changed": changed})

    def make_bad_request(self, error):
        return HttpResponse(error, status=400)


def trigger_door():
    # close the relay temporarily then re-open it to trigger the door to close
    pass