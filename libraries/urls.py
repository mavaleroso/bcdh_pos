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

    # company ----------------->

    path('company', views.company, name='company-list'),
    path('company_add', views.company_add, name='company-add'),
    path('company_edit', views.company_edit, name='company-edit'),
    path('company_update', views.company_update, name='company-update'),
    path('company_load', views.company_load, name='company-load'),






    # path('company', views.company, name='company-list'),
    path('addcompany', views.addcompany, name='add-company'),
    path('updatecompany', views.updatecompany, name='update-company'),
    # end --------------------->
    

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
]
