from django.views import View


class ControlView(View):
    def post(self):
        return "potato"