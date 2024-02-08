from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

MAX_NAME_LENGTH = 50
ELEMENTAL_CHOICES = {
    'F': 'Fire',
    'W': 'Water',
    'A': 'Wind',
    'E': 'Earth',
    'L': 'Light',
    'D': 'Dark',
    'M': 'Metal',
    'N': 'Nature'
}


class Equipment(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    image = models.ImageField(upload_to='images/equipment')
    category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE)
    minimum_level = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(199)])
    gold_value = models.PositiveIntegerField(default=0)
    durability = models.PositiveIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=1)
    enchantable = models.BooleanField(default=False)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    stats = models.ForeignKey('Stats', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(default=None, null=True, blank=True)


class ItemCategory(models.Model):
    ITEM_CATEGORIES = {
        'AC': 'Accessory',
        'BE': 'Belt',
        'BO': 'Boots',
        'EA': 'Earrings',
        'GA': 'Gauntlet',
        'GR': 'Greaves',
        'HE': 'Helmet',
        'NE': 'Necklace',
        'RI': 'Ring',
        'SH': 'Shield'
    }
    category_name = models.CharField(max_length=2, choices=ITEM_CATEGORIES)


class Weapon(Equipment):
    two_handed = models.BooleanField(default=False)
    damage_small_minimum = models.PositiveSmallIntegerField(default=1)
    damage_small_maximum = models.PositiveSmallIntegerField(default=1)
    damage_large_minimum = models.PositiveSmallIntegerField(default=1)
    damage_large_maximum = models.PositiveSmallIntegerField(default=1)


class Armor(Equipment):
    tailorable = models.BooleanField(default=False)
    dyeable = models.BooleanField(default=False)


class Skill(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)


class Spell(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)


class Trinket(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)


class Location(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)


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
