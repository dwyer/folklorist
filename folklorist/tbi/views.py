from urllib.parse import unquote

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Ballad, BalladIndex, BalladName, SuppTradFile
from .utils import query_to_words


def index_view(request):
    return render(request, 'home.html')


def search_view(request):
    limit = 30

    query = request.GET.get('q')
    page = int(request.GET.get('p', 1))
    start = int(request.GET.get('start', 1))

    info = None
    error = None
    pages = None
    finish = None

    if query:
        query = query.strip()
        title = 'Search for %s - Folklorist' % query
        results = BalladIndex.objects.all()
        words = query_to_words(query)
        results = results.filter(index__contains=words)
        num_results = results.count()
        offset = (page-1) * limit
        results = results[offset:offset+limit]

        if results:
            # pagination
            pages = []
            if page > 1:
                pages.append((
                    '/search?q=%s&p=%d' % (query, page-1),
                    'Previous',
                ))
            if len(results) == limit:
                pages.append((
                    "/search?q=%s&p=%d" % (query, page+1),
                    'Next',
                ))
            # love!
            start = offset + 1
            finish = offset + limit
    context = {
        'results': results,
        'pages': pages,
        'start': start,
        'finish': finish,
        'num_results': num_results,
        'query': query,
        'error': error,
        'info': info,
    }
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
