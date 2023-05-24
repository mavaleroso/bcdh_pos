from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Stocks, Clients, ClientType, Discounts, Sales, Payment,OutItems,SystemConfiguration)
import json 
from django.core import serializers
from datetime import date, datetime
from django.contrib.auth.hashers import make_password

from django.db.models import F

@csrf_exempt
def salestransaction(request):
    context = {
		'clients' : Clients.objects.filter().order_by('first_name'),
        'items' : Stocks.objects.filter().exclude(pcs_quantity=0).select_related(),
        'discount' : Discounts.objects.filter(),
        'client_type' : ClientType.objects.filter()
        
	}
    return render(request, 'sales/transaction.html', context)

@csrf_exempt
def saleslist(request):
    context = {
        'sales' : Sales.objects.filter().select_related()
	}
    return render(request, 'sales/list.html', context)
    
    
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
def patientalldetails(request):
    qs_list = list(
         (Clients.objects
             .filter()
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

def generate_code():
    inventory_code = SystemConfiguration.objects.values_list(
        'transaction_code', flat=True).first()
    
    last_code = inventory_code.split('-')
    sampleDate = date.today()
    year = sampleDate.strftime("%y")
    month = sampleDate.strftime("%m")
    series = 1

    if last_code[1] == month:
        series = int(last_code[2]) + 1

    code = year + '-' + month + '-' + f'{series:05d}'

    return code


@csrf_exempt
def salesitem(request):
    if request.method == 'POST':
        clie_id = request.POST.get('cl_id')
        disc_id = request.POST.get('dis_id')
        usr_id = request.session.get('user_id', 0)
        amt_paid = request.POST.get('amt_paid')
        sales_remarks = request.POST.get('remarks')
        stock_list = json.loads(request.POST.get('out_stocks'))
        code = generate_code()
        is_emergency = request.POST.get('is_emergency')
        pmt_type = request.POST.get('payment_type')
        
        if disc_id =="0":
            disc_id = None
        
        addsales = Sales(transaction_code = code,is_er=is_emergency,remarks=sales_remarks,client_id = clie_id,discount_id = disc_id, user_id = usr_id, payment_type = pmt_type)
        addsales.save()

        if Sales.id:
            system_config = SystemConfiguration.objects.first()
            system_config.transaction_code = code
            system_config.save()

        addpayment = Payment(amount_paid = amt_paid,sales_id = Sales.objects.last().id)
        addpayment.save()
        
        for stock_list_item in stock_list:
            price = float(stock_list_item['price'])*float(stock_list_item['quantity'])*float(stock_list_item['discount'])/100
            obj, was_created_bool = OutItems.objects.get_or_create(
            stock_id=stock_list_item['id'],
            quantity=stock_list_item['quantity'],
            discounted_amount=price,
            sales_id = Sales.objects.last().id
        )
            mainquantity=stock_list_item['stocksquantity']
            newquantity = stock_list_item['quantity']
            total_quantity = (int(mainquantity) - int(newquantity))
            Stocks.objects.filter(id=stock_list_item['id']).update(pcs_quantity=total_quantity)
        return JsonResponse({'data': 'success'})
    else:
        return JsonResponse({'data': 'error'})
    
    
@csrf_exempt
def addclient(request):
    
    firstname = request.POST.get('firstname')
    middlename = request.POST.get('middlename')
    lastname = request.POST.get('lastname')
    bdate = request.POST.get('birthdate')
    sex = request.POST.get('sex')
    address = request.POST.get('address')
    client_type = request.POST.get('client_type')
    occupation = request.POST.get('occupation')    
    
    addclt = Clients(first_name=firstname,middle_name=middlename,last_name = lastname,birthdate = bdate, sex=sex,address = address,occupation = occupation, client_type_id = client_type )
    addclt.save()

    return JsonResponse({'data': 'success'})



        





