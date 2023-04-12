from django.urls import path

from . import views

urlpatterns = [
    path('company', views.company, name='company-list'),
    path('user', views.user, name='user-list'),
    path('brand', views.brand, name='brand-list'),
    path('generic', views.generic, name='generic-list'),
    path('subgeneric', views.subgeneric, name='sub-generic-list'),
]
