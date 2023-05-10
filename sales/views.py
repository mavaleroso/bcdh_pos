from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Clients, Items, Discounts, Sales, Payment)
import json 
from django.core import serializers
import datetime
from django.contrib.auth.hashers import make_password

from django.db.models import F

@csrf_exempt
def salestransaction(request):
    context = {
		'clients' : Clients.objects.filter().order_by('first_name'),
        'items' : Items.objects.filter().exclude(pcs_quantity=0).select_related(),
        'discount' : Discounts.objects.filter()
        
	}
    return render(request, 'sales/transaction.html', context)

    
@csrf_exempt
def patientdetails(request):
    patient_id = request.POST.get('patient')
    qs_list = list(
         (Clients.objects
             .filter(id=patient_id)
             .select_related('client_type')
             .values('id','first_name','middle_name','last_name', 'client_type__name')
         )
    )
    return JsonResponse({'data': qs_list})


@csrf_exempt
def discountdetails(request):
    discount_id = request.POST.get('dis_id')
    qs_list = list(
         (Discounts.objects
             .filter(id=discount_id)
             .values('id','name','percentage')
         )
    )
    return JsonResponse({'data': qs_list})


@csrf_exempt
def salesitem(request):
    if request.method == 'POST':
        clie_id = request.POST.get('cl_id')
        disc_id = request.POST.get('dis_id')
        usr_id = request.session.get('user_id', 0)
        amt_paid = request.POST.get('amt_paid')

        if disc_id =="0":
            disc_id = None
            print("zero ni")
            print(disc_id)

        print("zero ni111")
        print(disc_id)
        
        addsales = Sales(is_er=False,client_id = clie_id,discount_id=disc_id,user_id = usr_id)
        addsales.save()
        addpayment = Payment(amount_paid = amt_paid,sales_id = Sales.objects.last().id)
        addpayment.save()

        return JsonResponse({'data': 'success'})
    else:
        return JsonResponse({'data': 'error'})



        





