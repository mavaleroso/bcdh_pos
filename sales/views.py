from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Stocks, StocksItems, Clients, ClientType, Discounts,
                         Sales, Payment, OutItems, SystemConfiguration, UserDetails, RoleDetails, Location)
import json
from django.core import serializers
from datetime import date, datetime
from django.contrib.auth.hashers import make_password

from django.db.models import F


def get_user_details(request):
    return UserDetails.objects.filter(user_id=request.user.id).first()


@login_required(login_url='login')
@csrf_exempt
def salestransaction(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Sales Staff", "Admin"]

    if role.role_name in allowed_roles:
        context = {
            'clients': Clients.objects.filter().order_by('first_name'),
            'items': StocksItems.objects.filter().exclude(pcs_quantity=0).select_related(),
            'discount': Discounts.objects.filter(),
            'client_type': ClientType.objects.filter(),
            'role_permission': role.role_name,
            'location': Location.objects.filter().order_by('id'),
        }
        return render(request, 'sales/transaction.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
@csrf_exempt
def saleslist(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Sales Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'sales': Sales.objects.filter().select_related(),
            'role_permission': role.role_name,
        }
        return render(request, 'sales/list.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
@csrf_exempt
def patientdetails(request):
    patient_id = request.POST.get('patient')
    qs_list = list(
        (Clients.objects
         .filter(id=patient_id)
         .select_related('client_type')
         .values('id', 'first_name', 'middle_name', 'last_name', 'client_type__name')
         )
    )
    return JsonResponse({'data': qs_list})


@login_required(login_url='login')
@csrf_exempt
def patientalldetails(request):
    qs_list = list(
        (Clients.objects
         .filter()
         .select_related('client_type')
         .values('id', 'first_name', 'middle_name', 'last_name', 'client_type__name')
         )
    )
    return JsonResponse({'data': qs_list})


@login_required(login_url='login')
@csrf_exempt
def discountdetails(request):
    discount_id = request.POST.get('dis_id')
    qs_list = list(
        (Discounts.objects
         .filter(id=discount_id)
         .values('id', 'name', 'percentage')
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
        client_id = request.POST.get('cl_id')
        discount_id = request.POST.get('dis_id')
        user_id = request.session.get('user_id', 0)
        amt_paid = request.POST.get('amt_paid')
        sales_remarks = request.POST.get('remarks')
        emergency_amt = request.POST.get('emergency_amt', 0)
        stock_list = json.loads(request.POST.get('out_stocks'))
        code = generate_code()
        is_emergency = request.POST.get('is_emergency')
        payment_type = request.POST.get('payment_type')

        if discount_id == "0":
            discount_id = None

        addsales = Sales(transaction_code=code, is_er=is_emergency, remarks=sales_remarks, client_id=client_id,
                         discount_id=discount_id, user_id=user_id, payment_status=payment_type, exact_amount_paid=emergency_amt)
        addsales.save()

        if addsales.id:
            system_config = SystemConfiguration.objects.first()
            system_config.transaction_code = code
            system_config.save()

        addpayment = Payment(amount_paid=amt_paid,
                             sales_id=Sales.objects.last().id)
        addpayment.save()

        discount_data = Discounts.objects.filter(
            id=discount_id).first()

        discount_percentage = discount_data.percentage if discount_id else 0

        for sl in stock_list:
            discounted_price = float(sl['price'])*int(
                sl['qty'])*discount_percentage/100
            true_price = float(sl['price'])*int(
                sl['qty'])
            OutItems.objects.get_or_create(
                stock_item_id=sl['stock_item_id'],
                quantity=sl['qty'],
                location_id=sl['location_id'],
                discounted_amount=discounted_price if discount_id else true_price,
                sales_id=addsales.id,
            )
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

    addclt = Clients(first_name=firstname, middle_name=middlename, last_name=lastname,
                     birthdate=bdate, sex=sex, address=address, occupation=occupation, client_type_id=client_type)
    addclt.save()

    return JsonResponse({'data': 'success'})
