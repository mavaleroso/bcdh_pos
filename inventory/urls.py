from django.urls import path

from . import views

urlpatterns = [
    path('in', views.inventory_in, name='inventory-in'),
    path('list', views.inventory_list, name='inventory-list'),

]

