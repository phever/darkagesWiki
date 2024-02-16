from django.urls import reverse
from django.utils import timezone


def default_links() -> list[dict]:
    """
    the default nav links, html will be rendered

    nav = { 'text': 'Home', 'icon': 'fa-home', 'url': reverse('index') }

    parent_nav = { 'text': 'Home', 'icon': 'fa-home', 'children': list[nav] }

    :return: list of dicts containing 'nav' and 'parent_nav' dictionaries
    """
    return [
        {
            'text': 'Home',
            'icon': 'fa-home',
            'url': reverse('index')
        },
        {
            'text': 'Weapons',
            'icon': 'fa-baseball-bat-ball',
            'url': reverse('weapons')
        },
        {
            'text': 'Armors',
            'icon': 'fa-shirt',
            'url': reverse('armors')
        },
        {
            'text': 'Equipment',
            'icon': 'fa-crown',
            'url': reverse('equipment')
        },
        # {
        #     'text': 'Skills',
        #     'icon': 'fa-dumbbell',
        #     'url': reverse('skills')
        # },
        # {
        #     'text': 'Spells',
        #     'icon': 'fa-wand-sparkles',
        #     'url': reverse('spells')
        # },
        {
            'header': 'Classes',
            'icon': '',
            'collapse': True,
            'children': [
                {
                    'text': 'Warrior',
                    'icon': 'fa-shield',
                    'url': reverse('warrior')
                },
                {
                    'text': 'Rogue',
                    'icon': 'fa-unlock-keyhole',
                    'url': reverse('rogue')
                },
                {
                    'text': 'Wizard',
                    'icon': 'fa-hat-wizard',
                    'url': reverse('wizard')
                },
                {
                    'text': 'Priest',
                    'icon': 'fa-cross',
                    'url': reverse('priest')
                },
                {
                    'text': 'Monk',
                    'icon': 'fa-hand-fist',
                    'url': reverse('monk')
                },
                {
                    'text': 'Peasant',
                    'icon': 'fa-piggy-bank',
                    'url': reverse('peasant')
                },
            ]
        },
        {
            'text': 'Items',
            'icon': 'fa-coins',
            'url': reverse('items')
        },
        {
            'text': 'Quests',
            'icon': 'fa-book',
            'url': reverse('quests')
        },
        {
            'text': 'Knowledge',
            'icon': 'fa-brain',
            'url': reverse('knowledge')
        },
    ]


def base_context(context: dict) -> dict:
    """
    adds context variables needed for every (base) template
    :param context:
    :return: context
    """
    def context_check(key) -> bool:
        """
        returns true if the context[key] is empty
        :param key:
        :return: bool
        """
        return key not in context

    # add sidebar/header/nav
    if context_check('nav_links'):
        context['nav_links'] = default_links()
    else:
        context['nav_links'] = default_links() + context['nav_links']

    # add current year for footer
    if context_check('current_year'):
        context['current_year'] = timezone.now().year

    return context
