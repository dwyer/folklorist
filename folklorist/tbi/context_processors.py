import string


def __make_func():
    linkpair_list = [(f'/search?q=startswith:{ch}', ch)
                     for ch in string.ascii_uppercase]
    context = {
        'letter_linkpair_list': linkpair_list,
    }
    def func(request):
        return context.copy()
    return func


alphanum_nav = __make_func()
