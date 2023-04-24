from django.urls import path

from . import views

urlpatterns = [
    path('company', views.company, name='company-list'),
    path('user', views.user, name='user-list'),
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
