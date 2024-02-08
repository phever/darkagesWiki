from django.conf import settings
from django.shortcuts import render


def index(request):
    context = {
        'title': f'Welcome to {settings.SITE_NAME}'
    }
    return render(request, 'index.html', context)
