from django.forms import ModelForm
from wiki.models import (
    Article,
    Item,
    Equipment,
    Weapon,
    Armor,
    SkillSpell,
    Location,
    Map,
    Quest,
    QuestStep,
)


class ArticleBaseForm(ModelForm):
    class Meta:
        model = Article
        exclude = ["author", "created", "last_edited", "approved_by"]


class ItemForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = Item


class EquipmentForm(ItemForm):
    class Meta(ItemForm.Meta):
        model = Equipment


class WeaponForm(EquipmentForm):
    class Meta(EquipmentForm.Meta):
        model = Weapon


class ArmorForm(EquipmentForm):
    class Meta(EquipmentForm.Meta):
        model = Armor


class SkillSpellForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = SkillSpell


class LocationForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = Location


class MapForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = Map


class QuestForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = Quest


class QuestStepForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = QuestStep


class ArticleForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        model = Article
        fields = ["name", "published"]
