from django.urls import reverse
from django.utils import timezone


def base_context(context):
    def context_check(key):
        return key not in context

    context['nav_links'] = [
        {
            'text': 'Home',
            'icon': 'fa-home',
            'url': reverse('index')
        },
        {
            'text': 'Weapons',
            'icon': 'fa-wand-sparkles',
            'url': reverse('index')
        },
        {
            'text': 'Armors',
            'icon': 'fa-vest',
            'url': reverse('index')
        },
        {
            'text': 'Equipment',
            'icon': 'fa-shield',
            'url': reverse('index')
        },
    ]
    if context_check('current_year'):
        context['current_year'] = timezone.now().year

    return context
