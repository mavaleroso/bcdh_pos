from django.urls import path

from . import views

urlpatterns = [
    path('item', views.item, name='item-list'),
    path('item_add', views.item_add, name='item-add'),
    path('item_edit', views.item_edit, name='item-edit'),
    path('item_load', views.item_load, name='item-load'),
]
