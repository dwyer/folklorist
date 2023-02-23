import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'folklorist.settings'
django.setup()

from tbi.models import Ballad

for child in Ballad.objects.order_by('name'):
    print('https://folklorist.org' + child.url())
