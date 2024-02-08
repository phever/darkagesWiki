from django.utils import timezone


def base_context(context):
    def context_check(key):
        return key not in context

    if context_check('current_year'):
        context['current_year'] = timezone.now().year

    return context
