from django.conf.urls import url
from garageControl.status import StatusView
from garageControl.control import ControlView

urlpatterns = [
    url(r'^status$', StatusView.as_view()),
    url(r'^control$', ControlView.as_view()),
]
