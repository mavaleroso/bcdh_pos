from django.urls import path

from . import views

urlpatterns = [
    path('transaction', views.salestransaction, name='sales-transaction'),
    path('patientdetails', views.patientdetails, name='patient-details'),
    path('discountdetails', views.discountdetails, name='discount-details'),
    path('salesitem', views.salesitem, name='sales-item'),
    path('addclient', views.addclient, name='add-client'),
    
]
