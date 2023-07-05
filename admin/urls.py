from django.urls import path

from . import views

urlpatterns = [

    path('clients', views.clients, name='clients-list'),
    path('user', views.user, name='user-list'),
    path('adduser', views.adduser, name='add-user'),
    path('updateuser', views.updateuser, name='update-user'),
    path('addclients', views.addclients, name='add-clients'),
    path('updateclients', views.updateclients, name='update-clients'),
    
    
    

]
