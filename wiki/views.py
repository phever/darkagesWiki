from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from . import forms
from .functions import base_context
from .models import Article, Weapon, Armor, Equipment


def index(request):
    context = {
        'title': f'Welcome to the {settings.SITE_NAME}',
    }
    return render(request, 'index.html', base_context(context))


def handler500(request, *args, **kwargs):
    return render(request, '404.html', base_context({}), status=500)


def handler404(request, exception, template_name='404.html'):
    return render(request, '404.html', base_context({}), status=404)


def weapons(request):
    context = {
        'title': f'{settings.SITE_NAME} - Weapons',
        'weapons': Weapon.objects.all()
    }
    return render(request, 'weapons.html', base_context(context))


def armor(request):
    context = {
        'title': f'{settings.SITE_NAME} - Armor',
        'armors': Armor.objects.all()
    }
    return render(request, 'armor.html', base_context(context))


def equipment(request):
    context = {
        'title': f'{settings.SITE_NAME} - Equipment',
        'equipments': Equipment.objects.all()
    }
    return render(request, 'equipment.html', base_context(context))


def skills(request):
    return None


def spells(request):
    return None


def knowledge(request):
    return None


def quests(request):
    return None


# def warrior(request):
#     return None
#
#
# def wizard(request):
#     return None
#
#
# def priest(request):
#     return None
#
#
# def rogue(request):
#     return None
#
#
# def monk(request):
#     return None
#
#
# def peasant(request):
#     return None


def items(request):
    return None


def new_weapon(request):
    context = {
        'title': 'Add a new Weapon',
        'form': forms.NewWeaponForm
    }
    return render(request, 'editors/new_article.html', base_context(context))


def new_armor(request):
    return None


def new_equipment(request):
    return None


def new_knowledge(request):
    return None


def new_spell(request):
    return None


def new_skill(request):
    return None


def new_item(request):
    return None


def new_quest(request):
    return None


@login_required
def article_form(request, pk=None):
    article = get_object_or_404(Article, pk=pk) if pk else None
    if request.method == "POST":
        form = forms.ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            if not article.pk:
                article.author = request.user
            article.save()
            return redirect("index")
    else:
        form = forms.ArticleForm(instance=article)

    context = {
        "title": "Edit Article" if pk else "New Article",
        "form": form,
    }
    return render(request, "editors/new_article.html", base_context(context))
