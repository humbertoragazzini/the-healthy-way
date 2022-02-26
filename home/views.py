from django.shortcuts import render

# Create your views here.


def index(request):
    """ view to return de index page """
    return render(request, 'home/index.html')
