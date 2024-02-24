from django.forms import ModelForm
from wiki.models import Weapon, Item


class NewWeaponForm(ModelForm):
    class Meta(object):
        model = Weapon


class NewItemForm(ModelForm):
    class Meta(object):
        model = Item


