import os, sys
import json

import django
from django.db import transaction
from django.db.utils import DataError

os.environ['DJANGO_SETTINGS_MODULE'] = 'folklorist.settings'
django.setup()

from tbi.models import Ballad, BalladIndex, BalladName, SuppTradFile


jsondir = sys.argv[1]

models = {
    'Ballad': Ballad,
    'BalladIndex': BalladIndex,
    'BalladName': BalladName,
    'SuppTradFile': SuppTradFile,
}

def visit(typ, obj):
    for model_name in models:
        try:
            for pk, sub in obj.pop(model_name).items():
                visit(model_name, sub)
        except KeyError:
            pass
    model = models[typ]
    if model and obj:
        try:
            instance = model(**obj)
            instance.save()
        except DataError:
            print(model)
            for key, val in obj.items():
                print(key, len(val), val)
            raise


for model in models.values():
    if model:
        print('deleting', model, model.objects.all().delete())

with transaction.atomic():
    for filename in os.listdir(jsondir):
        path = os.path.join(jsondir, filename)
        with open(path) as fp:
            data = json.load(fp)
        for typ, val in data.items():
            for pk, val in val.items():
                visit(typ, val)
