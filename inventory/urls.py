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
    path('received_item_load', views.received_item_load, name='received-item-load'),
]
