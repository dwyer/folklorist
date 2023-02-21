from django.conf import settings
from django.urls import path

from tbi.views import Search, ballad_view, index_view, sitemap_view

urlpatterns = [
    path('song/<encoded_title>', ballad_view),
    path('sitemaps/<start>.xml', sitemap_view),
    path('search', Search.as_view(), name='search'),
    path('', index_view),
]

if settings.DEBUG:
    from django.contrib import admin
    urlpatterns.append(path('admin/', admin.site.urls))
