from django.urls import path

from . import views

urlpatterns = [
    path('in', views.inventory_in, name='inventory-in'),
    path('store_items', views.store_items, name='store-items'),
]
