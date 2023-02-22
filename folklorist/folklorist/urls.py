from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from tbi.views import BalladDetail, Index, SearchPage, SitemapPage

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('search', SearchPage.as_view(), name='search'),
    path('song/<path:encoded_title>', BalladDetail.as_view(), name='ballad_detail'),
    path('sitemaps/<start>.xml', SitemapPage.as_view()),
]

if settings.DEBUG:
    from django.contrib import admin
    urlpatterns.append(path('admin/', admin.site.urls))
