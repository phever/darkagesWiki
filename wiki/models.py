from django.contrib.auth.models import User
from .model_constants import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='articles')
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approved_articles')


class Item(Article):
    category = models.CharField(max_length=2, choices=ITEM_CATEGORY_CHOICES)
    image = models.ImageField(upload_to=f'static/images/item/{category}')
    is_stackable = models.BooleanField(default=False)
    stack_size = models.PositiveIntegerField(default=None, null=True, blank=True)
    effect = models.TextField(default=None, null=True, blank=True)
    unidentified_name = models.CharField(max_length=MAX_NAME_LENGTH, null=True, blank=True)


class Equipment(Item):
    slot = models.CharField(choices=EQUIPMENT_CATEGORY_CHOICES, max_length=2)
    minimum_level = models.PositiveSmallIntegerField(default=1,
                                                     validators=[MinValueValidator(1), MaxValueValidator(199)])
    wearable_by_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    wearable_by_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    gold_value = models.PositiveIntegerField(default=0)
    durability = models.PositiveIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=1)
    armor_class = models.PositiveSmallIntegerField(default=0)
    is_enchantable = models.BooleanField(default=False)
    is_skin = models.BooleanField(default=False)
    is_perishable = models.BooleanField(default=False)
    location = models.ManyToManyField('Map', blank=True, default=None)
    stats = models.ForeignKey('Stats', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    notes = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Weapon(Equipment):
    is_two_handed = models.BooleanField(default=False)
    is_smithable = models.BooleanField(default=False)
    damage_small_minimum = models.PositiveSmallIntegerField(default=1)
    damage_small_maximum = models.PositiveSmallIntegerField(default=1)
    damage_large_minimum = models.PositiveSmallIntegerField(default=1)
    damage_large_maximum = models.PositiveSmallIntegerField(default=1)


class Armor(Equipment):
    is_tailorable = models.BooleanField(default=False)
    is_dyeable = models.BooleanField(default=False)


class SkillSpell(Article):
    spell_type = models.CharField(max_length=2, choices=SPELL_SKILL_TYPES)
    learned_by = models.CharField(max_length=2, choices=CLASS_CHOICES)
    image = models.ImageField(upload_to='static/images/skills_and_spells')
    minimum_level = models.PositiveSmallIntegerField(default=1,
                                                     validators=[MinValueValidator(1), MaxValueValidator(199)])
    required_strength = models.SmallIntegerField(default=0)
    required_constitution = models.SmallIntegerField(default=0)
    required_wisdom = models.SmallIntegerField(default=0)
    required_intelligence = models.SmallIntegerField(default=0)
    required_dexterity = models.SmallIntegerField(default=0)
    cooldown = models.SmallIntegerField(default=0)
    lines = models.SmallIntegerField(default=0)
    mana_cost = models.SmallIntegerField(default=0)
    description = models.TextField()


class SkillSpellRequirements(models.Model):
    linked_ability = models.ForeignKey('SkillSpell', on_delete=models.CASCADE)
    minimum_level = models.PositiveSmallIntegerField(default=1,
                                                     validators=[MinValueValidator(1), MaxValueValidator(199)])


class ItemRequirements(models.Model):
    linked_ability = models.ForeignKey('SkillSpell', on_delete=models.CASCADE)
    linked_item = models.ForeignKey('Item', on_delete=models.CASCADE)


class Location(Article):
    pass


class Map(Article):
    floor_a = models.PositiveSmallIntegerField(default=1)
    floor_b = models.PositiveSmallIntegerField(default=1)
    area = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.floor_a}-{self.floor_b}'


class Stats(models.Model):
    offense = models.CharField(choices=ELEMENTAL_CHOICES, max_length=1, null=True, blank=True, default=None)
    defense = models.CharField(choices=ELEMENTAL_CHOICES, max_length=1, null=True, blank=True, default=None)
    armor_class = models.SmallIntegerField(default=0)
    strength = models.SmallIntegerField(default=0)
    constitution = models.SmallIntegerField(default=0)
    wisdom = models.SmallIntegerField(default=0)
    intelligence = models.SmallIntegerField(default=0)
    dexterity = models.SmallIntegerField(default=0)
    regen = models.SmallIntegerField(default=0)
    health = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    hit = models.SmallIntegerField(default=0)
    damage = models.SmallIntegerField(default=0)
    magic_resist_percent = models.SmallIntegerField(default=0)


class Quest(Article):
    minimum_level = models.PositiveSmallIntegerField(default=1,
                                                     validators=[MinValueValidator(1), MaxValueValidator(199)])
    maximum_level = models.PositiveSmallIntegerField(default=None, null=True, blank=True,
                                                     validators=[MinValueValidator(1), MaxValueValidator(199)])
    repeatable = models.PositiveIntegerField(default=0, help_text="Repeatable every n hours")
    quest_start = models.ForeignKey('Location', on_delete=models.CASCADE)
    required_items = models.ManyToManyField('Article', related_name='quest_required_items')
    rewards = models.ManyToManyField('Article', related_name='quest_rewards')


class QuestStep(Article):
    related_quest = models.ForeignKey('Quest', on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    header = models.CharField(max_length=255)
    body = models.TextField()
