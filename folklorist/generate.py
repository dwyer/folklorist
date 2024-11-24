import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'folklorist.settings'
django.setup()

from tbi.models import Ballad, BalladName, BalladIndex
from tbi.utils import title_unquote


for bi in BalladIndex.objects.all():
    print(bi.name, bi.index)
exit()

with open('../404.txt') as fp:
    for line in fp:
        title = line.strip()
        name = title_unquote(title)
        try:
            b = Ballad.objects.get(name=name)
            bn, created = BalladName.objects.get_or_create(
                parent=b, name=b.name, title=b.title())
            print(created, bn, title)
            # bi, created = BalladIndex.objects.get_or_create(
            #     parent=bn, name=b.name, title=b.title())
        except Ballad.DoesNotExist as e:
            print('Ballad.DoesNotExist:', title)
        except BalladName.DoesNotExist as e:
            print('BalladName.DoesNotExist:', title)
        except BalladIndex.DoesNotExist as e:
            print('BalladIndex.DoesNotExist:', title)

exit()

for child in Ballad.objects.order_by('name'):
    print('https://folklorist.org' + child.url())
