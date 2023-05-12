from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Stocks, Clients, Items, Discounts, Sales, Payment,OutItems)
import json 
from django.core import serializers
import datetime
from django.contrib.auth.hashers import make_password

from django.db.models import F

@csrf_exempt
def salestransaction(request):
    context = {
		'clients' : Clients.objects.filter().order_by('first_name'),
        'items' : Stocks.objects.filter().exclude(pcs_quantity=0).select_related(),
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
        sales_remarks = request.POST.get('remarks')
        item_size = request.POST.get('item_size')

        out_items1 = request.POST.get('out_stocks')
        print("testniha")

        print(out_items1)
        for i in out_items1:
            print("onee")
            print(out_items1[i])

        

        # item_list  = request.POST["out_stocks"]
        # item_list = item_list.split(",")
        # print("itemmlistthisaaa")
        # print(out_items1)



        # for i in out_items1:
            
        #     # out_items = request.POST.getlist('out_stocks['+i+']')
        #     print("data_testa11")
        #     print(i)
        #     print("items ni")
        #     print(out_items1)
            

        

        # for i in range(item_size):
        #     out_items = request.POST.getlist('out_stocks['+i+']')
        #     print("data_testa")
        #     print(out_items)
        # print(item_size)
        # print(request.POST.getlist('out_stocks[]'))
        if disc_id =="0":
            disc_id = None
            print("zero ni")
            print(disc_id)

        addsales = Sales(is_er=0,remarks=sales_remarks,client_id = clie_id,discount_id=disc_id,user_id = usr_id)
        addsales.save()
        addpayment = Payment(amount_paid = amt_paid,sales_id = Sales.objects.last().id)
        addpayment.save()


        # stock = OutItems(quantity=qty,discounted_amount=sales_remarks,stock_id = clie_id)
        # stock.save()

        return JsonResponse({'data': 'success'})
    else:
        return JsonResponse({'data': 'error'})



        





