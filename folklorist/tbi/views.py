from urllib.parse import unquote

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render


from .models import Ballad, BalladIndex, BalladName, SuppTradFile
from .utils import query_to_words

PAGINATOR_LIMIT = 10


def index_view(request):
    return render(request, 'home.html')


def search_view(request):

    query = request.GET.get('q')
    page_number = int(request.GET.get('p', 1))
    # start = int(request.GET.get('start', 1))

    context = {
        'query': query,
    }

    def get_page_url(page_number):
        return '/search?q=%s&p=%s' % (query, page_number)

    if query:
        query = query.strip()
        results = BalladIndex.objects.all()
        words = query_to_words(query)
        results = results.filter(index__contains=words).order_by('name')
        paginator = Paginator(results, PAGINATOR_LIMIT)
        page = paginator.page(page_number)
        page_urls = []
        if page.has_previous():
            page_urls.append((get_page_url(page.previous_page_number()), 'Previous'))
        if page.has_previous():
            page_urls.append((get_page_url(page.next_page_number()), 'Next'))
        context.update({
            'page_obj': page,
            'page_urls': page_urls,
            'title': 'Search for %s - Folklorist' % query,
        })
    return render(request, 'search.html', context)


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
    return render(request, 'sitemap.xml', context, content_type='text/xml')
