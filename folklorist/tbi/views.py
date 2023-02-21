from urllib.parse import unquote

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

from .models import Ballad, BalladIndex, BalladName, SuppTradFile
from .utils import query_to_words

PAGINATOR_LIMIT = 10


index_view = TemplateView.as_view(template_name='home.html')


class Search(ListView):
    template_name = 'search.html'
    model = BalladIndex
    ordering = 'name'
    paginate_by = PAGINATOR_LIMIT
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


def ballad_view(request, encoded_title):
    title = unquote(encoded_title.replace('_', ' '))
    ballad_name = get_object_or_404(BalladName, title=title)
    ballad = ballad_name.parent
    context = {
        'ballad': ballad,
        'title': ballad.title,
    }
    try:
        context['supptrad'] = SuppTradFile.objects.get(parent=ballad)
    except SuppTradFile.DoesNotExist:
        pass
    return render(request, 'ballad.html', context)


def sitemap_view(request, start):
    # TODO make these static
    end = start + chr(126)
    q = (BalladName.objects.filter(name__gte=start, name__lt=end)
         .order_by('name'))
    context = {'list': q}
    eturn render(request, 'sitemap.xml', context, content_type='text/xml')
