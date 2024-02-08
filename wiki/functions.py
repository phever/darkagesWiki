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
            'url': reverse('weapons')
        },
        {
            'text': 'Armors',
            'icon': 'fa-vest',
            'url': reverse('armors')
        },
        {
            'text': 'Equipment',
            'icon': 'fa-shield',
            'url': reverse('equipment')
        },
    ]
    if context_check('current_year'):
        context['current_year'] = timezone.now().year

    return context
