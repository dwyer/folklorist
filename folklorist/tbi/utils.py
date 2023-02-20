import re

from string import ascii_uppercase as letters


def alphabet():
    links = ['<a href="/search?q=startswith:%s">%s</a>' % (c, c) for c in letters]
    return ' &middot; '.join(links)


def query_to_words(query):
    query = query.lower()
    query = re.sub(r'[-/]', ' ', query)
    query = re.sub(r'[^\w\s\':]', '', query)
    return list(set(query.split()))
