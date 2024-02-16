from django.urls import path
from wiki import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weapons/', views.weapons, name='weapons'),
    path('armors/', views.armors, name='armors'),
    path('equipment/', views.equipment, name='equipment'),
    # path('skills/', views.skills, name='skills'),
    # path('spells/', views.spells, name='spells'),
    path('quests/', views.quests, name='quests'),
    path('knowledge/', views.knowledge, name='knowledge'),
    path('items/', views.items, name='items'),
    path('class/warrior/', views.warrior, name='warrior'),
    path('class/wizard/', views.wizard, name='wizard'),
    path('class/priest/', views.priest, name='priest'),
    path('class/rogue/', views.rogue, name='rogue'),
    path('class/monk/', views.monk, name='monk'),
    path('class/peasant/', views.peasant, name='peasant'),
    path('new/weapons/', views.new_weapon, name='new-weapon'),
    path('new/armors/', views.new_armor, name='new-armors'),
    path('new/equipment/', views.new_equipment, name='new-equipment'),
    path('new/skills/', views.new_skill, name='new-skill'),
    path('new/spells/', views.new_spell, name='new-spell'),
    path('new/quests/', views.new_quest, name='new-quest'),
    path('new/knowledge/', views.new_knowledge, name='new-knowledge'),
    path('new/items/', views.new_item, name='new-item'),
]
