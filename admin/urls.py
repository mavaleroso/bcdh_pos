from django.urls import path

from . import views

urlpatterns = [

    path('clients', views.clients, name='clients-list'),
    path('user', views.user, name='user-list'),
    path('adduser', views.adduser, name='add-user'),
    path('updateuser', views.updateuser, name='update-user'),
    path('addclients', views.addclients, name='add-clients'),
    path('updateclients', views.updateclients, name='update-clients'),


    
    path('user', views.user, name='user-list'),
    path('user_add', views.user_add, name='user-add'),
    path('user_edit', views.user_edit, name='user-edit'),
    path('user_update', views.user_update, name='user-update'),
    path('user_load', views.user_load, name='user-load'),
    
    
    

]
