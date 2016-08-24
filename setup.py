import pip
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "GarageWarden.settings"
pip.main(['install', '-r', str(os.path.abspath("requirements.txt"))])

import django
django.setup()
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

execute_from_command_line(["manage.py", "migrate"])
create_super = False
if User.objects.filter(is_superuser=True).exists():
    i = input("There is already at least one super user, would you like to create another (type y or n):")
    if i and i.lower()[0] == 'y':
        create_super = True
if create_super:
    execute_from_command_line(["manage.py", "createsuperuser"])
