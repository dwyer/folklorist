from urllib.parse import unquote

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Ballad, BalladIndex, BalladName, SuppTradFile
from .utils import query_to_words


class Index(TemplateView):
    template_name = 'home.html'


class SearchPage(ListView):
    template_name = 'search.html'
    model = BalladIndex
    ordering = 'name'
    paginate_by = 10
    page_kwarg = 'p'

    def get_search_query(self):
        return self.request.GET.get('q')

    def get_page_url(self, page_number):
        search_query = self.get_search_query()
        return '/search?q=%s&p=%s' % (search_query, page_number)

    def get_queryset(self):
        search_query = self.get_search_query()
        words = query_to_words(search_query)
        return super().get_queryset().filter(index__contains=words)

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
            'title': 'Search for %s - Folklorist' % search_query,
            'query': search_query,
            'page_urls': page_urls,
        })

        return kwargs


class BalladDetail(DetailView):
    template_name = 'ballad.html'
    context_object_name = 'ballad'

    def get_object(self):
        encoded_title = self.kwargs['encoded_title']
        title = unquote(encoded_title.replace('_', ' '))
        ballad_name = get_object_or_404(BalladName, title=title)
        ballad = ballad_name.parent
        return ballad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ballad = context['ballad']
        context.update({
            'title': ballad.title,
        })
        try:
            context['supptrad'] = SuppTradFile.objects.get(parent=ballad)
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
