from django.conf import settings
from django.shortcuts import render
from .functions import base_context


def index(request):
    context = {
        'title': f'Welcome to the {settings.SITE_NAME}'
    }
    return render(request, 'index.html', base_context(context))
