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
    # end --------------------->

    # brand ----------------->
    path('brand', views.brand, name='brand-list'),
    path('brand_add', views.brand_add, name='brand-add'),
    path('brand_edit', views.brand_edit, name='brand-edit'),
    path('brand_update', views.brand_update, name='brand-update'),
    path('brand_load', views.brand_load, name='brand-load'),
    # end --------------------->

    # generic ----------------->
    path('generic', views.generic, name='generic-list'),
    path('generic_add', views.generic_add, name='generic-add'),
    path('generic_edit', views.generic_edit, name='generic-edit'),
    path('generic_update', views.generic_update, name='generic-update'),
    path('generic_load', views.generic_load, name='generic-load'),
    # end --------------------->

    # subgeneric ----------------->
    # path('subgeneric', views.subgeneric, name='sub-generic-list'),
    # path('subgeneric_add', views.subgeneric_add, name='sub-generic-add'),
    # path('subgeneric_edit', views.subgeneric_edit, name='sub-generic-edit'),
    # path('subgeneric_update', views.subgeneric_update, name='sub-generic-update'),
    # path('subgeneric_load', views.subgeneric_load, name='sub-generic-load'),
    # end --------------------->
    
    path('subgeneric', views.subgeneric, name='sub-generic-list'),
    path('addsubgeneric', views.addsubgeneric, name='add-sub-generic'),
    path('updatesubgeneric', views.updatesubgeneric, name='update-sub-generic'),
    path('units', views.units, name='units-list'),
    path('units', views.addunits, name='add-units'),
    path('updateunits', views.updateunits, name='update-units'),
]
