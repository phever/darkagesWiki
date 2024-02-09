from django.conf import settings
from django.shortcuts import render
from .functions import base_context


def index(request):
    context = {
        'title': f'Welcome to the {settings.SITE_NAME}',
    }
    return render(request, 'index.html', base_context(context))


def weapons(request):
    pass


def armors(request):
    pass


def equipment(request):
    pass


def skills(request):
    return None


def spells(request):
    return None


def knowledge(request):
    return None


def quests(request):
    return None


def warrior(request):
    return None


def wizard(request):
    return None


def priest(request):
    return None


def rogue(request):
    return None


def monk(request):
    return None


def peasant(request):
    return None


def items(request):
    return None
