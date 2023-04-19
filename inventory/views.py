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
from main.models import (Item, ItemDetails)


def inventory_in(request):
    return render(request, 'inventory/in.html')


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
        item_quantity = request.POST.get('ItemQuantity')
        item_quantity_pcs = request.POST.get('ItemQuantityPcs')
        total_quantity_pcs = request.POST.get('TotalQuantityPcs')
        retail_price_unit = request.POST.get('RetailPriceUnit')
        retail_price_pcs = request.POST.get('RetailPricePcs')
        user_id = request.session.get('user_id', 0)

        add = Item(type_id=item_type, company_id=company, generic_id=generic, sub_generic_id=sub_generic,
                   description=description, brand_id=brand, unit_price=unit_price, unit_id=item_unit, unit_quantity=item_quantity, retail_price_unit=retail_price_unit, retail_price=retail_price_pcs, user_id=user_id)
        add.save()
        return JsonResponse({'data': 'success'})
