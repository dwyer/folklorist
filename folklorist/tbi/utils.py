import urllib.parse

URL_SAFE_CHARS = '/()\','


def title_quote(text):
    return urllib.parse.quote(text.replace(' ', '_'), safe=URL_SAFE_CHARS)


def title_unquote(text):
    return urllib.parse.unquote(text.replace('_', ' '))
