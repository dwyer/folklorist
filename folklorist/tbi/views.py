import re

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView

from .mixins import TitleMixin
from .models import Ballad, BalladIndex, BalladName, SuppTradFile
from .utils import title_unquote


class Index(TemplateView):
    template_name = 'home.html'


class SearchPage(TitleMixin, ListView):
    template_name = 'search.html'
    model = BalladIndex
    ordering = 'name'
    paginate_by = 10
    page_kwarg = 'p'

    def get_search_query(self):
        return self.request.GET.get('q', '')

    def get_search_query_tokens(self):
        query = self.get_search_query().lower()
        query = re.sub(r'[-/]', ' ', query)
        query = re.sub(r'[^\w\s\':]', '', query)
        return list(set(query.split()))

    def get_title(self):
        return 'Search for %s' % self.get_search_query()

    def get_page_url(self, page_number):
        search_query = self.get_search_query()
        return '%s?q=%s&p=%s' % (reverse('search'), search_query, page_number)

    def get_queryset(self):
        tokens = self.get_search_query_tokens()
        return super().get_queryset().filter(index__contains=tokens)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        search_query = self.get_search_query()

        page = kwargs['page_obj']
        page_urls = []
        if page.has_previous():
            page_urls.append(
                (self.get_page_url(page.previous_page_number()), 'Previous'))
        if page.has_next():
            page_urls.append(
                (self.get_page_url(page.next_page_number()), 'Next'))
        kwargs.update({
            'page_urls': page_urls,
            'search_query': search_query,
        })

        return kwargs


class BalladDetail(TitleMixin, DetailView):
    template_name = 'ballad.html'
    context_object_name = 'ballad'

    def get_object(self):
        title = title_unquote(self.kwargs['encoded_title'])
        try:
            ballad_name = get_object_or_404(BalladName, title__iexact=title)
        except BalladName.MultipleObjectsReturned:
            ballad_name = BalladName.objects.filter(title=title)[0]
        ballad = ballad_name.parent
        return ballad

    def get_title(self):
        return self.object.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['supptrad'] = SuppTradFile.objects.get(parent=self.object)
        except SuppTradFile.DoesNotExist:
            pass
        return context


class SitemapPage(ListView):
    model = BalladName
    ordering = 'name'
    template_name = 'sitemap.xml'
    content_type = 'text/xml'

    def get_queryset(self):
        start = self.kwargs['start']
        end = start + chr(126)
        return super().get_queryset().filter(name__gte=start, name__lt=end)
