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

def visit(typ, obj, parent=None):
    children = {}
    for model_name in models:
        try:
            children[model_name] = obj.pop(model_name)
        except KeyError:
            pass
    model = models[typ]
    if model and obj:
        try:
            if parent:
                obj['parent'] = parent
            instance = model(**obj)
            instance.save()
            for key, val in children.items():
                visit_all(key, val, parent=instance)
        except DataError:
            print(model)
            for key, val in obj.items():
                print(key, len(val), val)
            raise


def visit_all(typ, objs, parent=None):
    for pk, obj in objs.items():
        visit(typ, obj, parent=parent)


for model in models.values():
    if model:
        print('deleting', model, model.objects.all().delete())

with transaction.atomic():
    for filename in os.listdir(jsondir):
        path = os.path.join(jsondir, filename)
        with open(path) as fp:
            data = json.load(fp)
        for typ, val in data.items():
            visit_all(typ, val)
