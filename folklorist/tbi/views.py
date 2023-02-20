from django.shortcuts import render

from ballads.hacks import alphabet



def index_view(request):
    context = {'vols': alphabet()}
    return render(request, 'home.html', context)
