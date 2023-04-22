from django.urls import path

from . import views

urlpatterns = [
    path('company', views.company, name='company-list'),
    path('user', views.user, name='user-list'),
    path('brand', views.brand, name='brand-list'),
    path('generic', views.generic, name='generic-list'),
    path('subgeneric', views.subgeneric, name='sub-generic-list'),
    path('addgeneric', views.addgeneric, name='add-generic'),
    path('updategeneric', views.updategeneric, name='update-generic'),
    path('addcompany', views.addcompany, name='add-company'),
    path('updatecompany', views.updatecompany, name='update-company'),
]
