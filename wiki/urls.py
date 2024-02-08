from django.urls import path
from wiki import views

urlpatterns = [
    path('', views.index, name='index')
]
