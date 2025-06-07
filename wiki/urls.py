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
    path('article/new/', views.new_article, name='article-new'),
    path('new/weapon/', views.new_weapon, name='new-weapon'),
    path('article/edit/<int:pk>/', views.article_form, name='article-edit'),
]
