from django.urls import path
from wiki import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weapons/', views.weapons, name='weapons'),
    path('armors/', views.armors, name='armors'),
    path('equipment/', views.equipment, name='equipment')
]
