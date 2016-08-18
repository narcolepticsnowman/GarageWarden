import pip
import os

pip.main(['install', '-r', str(os.path.abspath("requirements.txt"))])

from django.core.management import execute_from_command_line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GarageWarden.settings")
execute_from_command_line(["manage.py", "migrate"])
execute_from_command_line(["manage.py", "createsuperuser"])
