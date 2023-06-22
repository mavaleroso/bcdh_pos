from django.urls import path
from . import views

urlpatterns = [
    path('in', views.inventory_in, name='inventory-in'),
    path('store_items', views.store_items, name='store-items'),
    path('update_stock/<int:stock_id>', views.update_stock, name='update-stock'),
    path('list', views.inventory_list, name='inventory-list'),
    path('list/edit/<int:stock_id>', views.inventory_list_edit,
         name='inventory-list-edit'),
    path('load', views.inventory_load, name='inventory-load'),
    path('export_excel', views.export_excel, name='export-excel'),
    path('po/list', views.inventory_po_list, name='inventory-po-list'),
    path('po/load', views.inventory_po_load, name='inventory-po-load'),
    path('po/list/export_excel', views.po_export_excel, name='po-export-excel'),
    path('po/view/<int:stock_id>', views.po_view, name='po-view'),
]
