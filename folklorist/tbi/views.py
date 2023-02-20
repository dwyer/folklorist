from django.db.models import Q
from django.shortcuts import render

from ballads.hacks import query_to_words

from .models import BalladIndex


def word_to_Q(w):
    # TODO handle split error
    kw, val = w.split(':')
    if kw == 'startswith':
        return Q(name__startswith=val)
    elif kw == 'keyword':
        return Q(keywords__contains=[val])
    return None


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
        for word in query_to_words(query):
            results = results.filter(word_to_Q(word))
        num_results = results.count()
        offset = (page-1) * limit
        results = results[offset:offset+limit]

        if results:
            # pagination
            pages = []
            if page > 1:
              pages.append('<a href="/search?q=%s&p=%d">&lt; Previous</a>'
                  % (query, page-1))
            if len(results) == limit:
              pages.append('<a href="/search?q=%s&p=%d">Next &gt;</a>'
                  % (query, page+1))
            pages = ' &middot; '.join(pages)
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
