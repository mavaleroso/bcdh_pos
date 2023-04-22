from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Item, ItemDetails, SystemConfiguration)

import datetime


def inventory_in(request):
    return render(request, 'inventory/in.html')


def generate_code():
    inventory_code = SystemConfiguration.objects.values_list('inventory_code', flat=True).first()

    last_code = inventory_code.split('-')

    sampleDate = datetime.date.today()
    year = sampleDate.strftime("%y")
    month = sampleDate.strftime("%m")
    series = 1

    if last_code[1] == month:
        series = int(last_code[2]) + 1

    code = year + '-' + month + '-' + f'{series:05d}'

    return code


@csrf_exempt
def store_items(request):
    if request.method == 'POST':
        item_type = request.POST.get('ItemType')
        company = request.POST.get('Company')
        generic = request.POST.get('Generic')
        sub_generic = request.POST.get('SubGeneric')
        description = request.POST.get('Description')
        brand = request.POST.get('Brand')
        unit_price = request.POST.get('UnitPrice')
        item_unit = request.POST.get('ItemUnit')
        item_quantity = request.POST.get('ItemQuantity') if request.POST.get('ItemQuantity') else 0
        item_quantity_pcs = request.POST.get('ItemQuantityPcs')
        total_quantity_pcs = request.POST.get('TotalQuantityPcs')
        retail_price_unit = request.POST.get('RetailPriceUnit') if request.POST.get('RetailPriceUnit') else 0
        retail_price_pcs = request.POST.get('RetailPricePcs')
        user_id = request.session.get('user_id', 0)
        code = generate_code()
       
        item_add = Item(code=code, type_id=item_type, company_id=company, generic_id=generic, sub_generic_id=sub_generic,
                        description=description, brand_id=brand, unit_price=unit_price, unit_id=item_unit, unit_quantity=item_quantity, retail_price_unit=retail_price_unit, retail_price=retail_price_pcs, user_id=user_id)

        item_add.save()

        if item_add.id:
            system_config = SystemConfiguration.objects.first()
            system_config.inventory_code = code
            system_config.save()

        counter = item_quantity if int(item_quantity) > 0 else total_quantity_pcs
        for i in range(int(counter)):
            barcode = request.POST.get('barcode['+str(i)+']')
            expiry_date = request.POST.get('expiryDate['+str(i)+']')
            item_details_add = ItemDetails(
                item_id=item_add.id, quantity=item_quantity_pcs, barcode=barcode, expiration_date=expiry_date)
            item_details_add.save()

        return JsonResponse({'data': 'success'})