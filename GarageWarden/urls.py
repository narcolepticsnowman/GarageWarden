"""GarageWarden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from GarageWarden.status import StatusView
from GarageWarden.control import ControlView
from GarageWarden.login import LoginView
from GarageWarden.logout import LogOutView
from GarageWarden.notify import test_email

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/garage/status', StatusView.as_view()),
    url(r'^api/garage/control', ControlView.as_view()),
    url(r'^api/login', LoginView.as_view()),
    url(r'^api/logout', LogOutView.as_view()),
    url(r'^email/test', test_email)
]
