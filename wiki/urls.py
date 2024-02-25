from django.urls import path
from wiki import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weapons/', views.weapons, name='weapons'),
    path('armor/', views.armor, name='armor'),
    path('equipment/', views.equipment, name='equipment'),
    path('skills/', views.skills, name='skills'),
    path('spells/', views.spells, name='spells'),
    path('quests/', views.quests, name='quests'),
    path('knowledge/', views.knowledge, name='knowledge'),
    path('items/', views.items, name='items'),
    # path('class/warrior/', views.warrior, name='warrior'),
    # path('class/wizard/', views.wizard, name='wizard'),
    # path('class/priest/', views.priest, name='priest'),
    # path('class/rogue/', views.rogue, name='rogue'),
    # path('class/monk/', views.monk, name='monk'),
    # path('class/peasant/', views.peasant, name='peasant'),
    path('new/weapon/', views.new_weapon, name='new-weapon'),
    path('new/armor/', views.new_armor, name='new-armors'),
    path('new/equipment/', views.new_equipment, name='new-equipment'),
    path('new/skill/', views.new_skill, name='new-skill'),
    path('new/spell/', views.new_spell, name='new-spell'),
    path('new/quest/', views.new_quest, name='new-quest'),
    path('new/knowledge/', views.new_knowledge, name='new-knowledge'),
    path('new/item/', views.new_item, name='new-item'),
]
