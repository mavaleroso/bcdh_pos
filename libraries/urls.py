from django.urls import path

from . import views

urlpatterns = [
    path('item', views.item, name='item-list'),
    path('item_add', views.item_add, name='item-add'),
    path('item_edit', views.item_edit, name='item-edit'),
    path('item_update', views.item_update, name='item-update'),
    path('item_load', views.item_load, name='item-load'),
    path('fetch_item_by_barcode', views.fetch_item_by_barcode,name='fetch-item-by-barcode'),
    path('item_collections', views.item_collections, name='item-collections'),
    
    path('company', views.company, name='company-list'),
    path('brand', views.brand, name='brand-list'),
    path('generic', views.generic, name='generic-list'),
    path('subgeneric', views.subgeneric, name='sub-generic-list'),
    path('units', views.units, name='units-list'),
    path('addgeneric', views.addgeneric, name='add-generic'),
    path('updategeneric', views.updategeneric, name='update-generic'),
    path('addbrand', views.addbrand, name='add-brand'),
    path('updatebrand', views.updatebrand, name='update-brand'),
    path('addsubgeneric', views.addsubgeneric, name='add-sub-generic'),
    path('updatesubgeneric', views.updatesubgeneric, name='update-sub-generic'),
    path('units', views.addunits, name='add-units'),
    path('updateunits', views.updateunits, name='update-units'),
    path('addcompany', views.addcompany, name='add-company'),
    path('updatecompany', views.updatecompany, name='update-company'),
]
