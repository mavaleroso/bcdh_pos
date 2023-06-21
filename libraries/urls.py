from django.urls import path

from . import views

urlpatterns = [
    path('item', views.item, name='item-list'),
    path('item_add', views.item_add, name='item-add'),
    path('item_edit', views.item_edit, name='item-edit'),
    path('item_update', views.item_update, name='item-update'),
    path('item_load', views.item_load, name='item-load'),
    path('fetch_item_by_barcode', views.fetch_item_by_barcode,
         name='fetch-item-by-barcode'),
    path('item_collections', views.item_collections, name='item-collections'),
]
