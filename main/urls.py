from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory/', include('inventory.urls')),
    path('admin/', include('admin.urls')),
    path('sales/', include('sales.urls')),
    path('management/', include('management.urls')),
]
