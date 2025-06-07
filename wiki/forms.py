import django.forms
from django.forms import ModelForm
from wiki.models import Article, Weapon, Item


class NewWeaponForm(ModelForm):
    class Meta(object):
        model = Weapon
        fields = django.forms.ALL_FIELDS


class NewItemForm(ModelForm):
    class Meta(object):
        model = Item
        fields = django.forms.ALL_FIELDS


class ArticleForm(ModelForm):
    """Create or edit an ``Article`` instance."""

    class Meta(object):
        model = Article
        # only expose editable fields
        fields = ["name", "published"]
