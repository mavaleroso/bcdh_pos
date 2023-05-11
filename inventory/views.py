from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from main.models import (Stocks, Items, SystemConfiguration, ItemType, Company, Generic, SubGeneric, Brand, Unit, AuthUser, OutItems)
from datetime import date, datetime
import math



def inventory_in(request):
    context = {
        'item_type': ItemType.objects.filter().order_by('name'),
        'company': Company.objects.filter().order_by('name'),
        'generic': Generic.objects.filter().order_by('name'),
        'sub_generic': SubGeneric.objects.filter().order_by('name'),
        'brand': Brand.objects.filter().order_by('name'),
        'item_unit': Unit.objects.filter().order_by('name'),
    }
    return render(request, 'inventory/in.html', context)


def inventory_list(request):
    return render(request, 'inventory/list.html')


def inventory_load(request):
    stock_data = Stocks.objects.select_related().order_by('-delivered_date').reverse()
    total = stock_data.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        stock_data = stock_data[start:start + length]

    data = []

    for stock in stock_data:
        userData = AuthUser.objects.filter(id=stock.user.id)
        outItemsData=OutItems.objects.filter(item_id=stock.id)
        full_name = userData[0].first_name + ' ' + userData[0].last_name

        expended_stock = 0

        for outItem in outItemsData:
            expended_stock = expended_stock + outItem.quantity

        available = stock.pcs_quantity - expended_stock

        expiration_aging = stock.expiration_date - datetime.now().date()

        item = {
            'id': stock.id,
            'code': stock.code,
            'barcode': stock.items.barcode,
            'details': stock.items.generic.name + ' ' + stock.items.sub_generic.name + ' ' + stock.items.classification + ' ' + stock.items.description, 
            'pcs_quantity': stock.pcs_quantity,
            'available_stock': stock,
            'unit_price': stock.unit_price,
            'retail_price': stock.retail_price,
            'expiration_date': stock.expiration_date,
            'expiration_aging': expiration_aging.days,
            'delivered_date': stock.delivered_date,
            'created_at': stock.created_at,
            'updated_at': stock.updated_at,
            'created_by': full_name
        }

        if available > 0:
            data.append(item)

    response = {
        'data': data,
        'page': page,
        'per_page': per_page,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


def generate_code():
    inventory_code = SystemConfiguration.objects.values_list(
        'inventory_code', flat=True).first()

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
def store_items(request):
    if request.method == 'POST':
        item_id = request.POST.get('ItemID')
        company = request.POST.get('Company')
        unit_price = request.POST.get('UnitPrice')
        item_quantity_pcs = request.POST.get('ItemQuantityPcs')
        retail_price = request.POST.get('RetailPricePcs')
        expiration_date = request.POST.get('ExpirationDate')
        delivery_date = request.POST.get('DeliveredDate')
        user_id = request.session.get('user_id', 0)
        code = generate_code()

        stocks = Stocks(code=code, item_id=item_id, company_id=company, unit_price=unit_price, pcs_quantity=item_quantity_pcs, retail_price=retail_price, delivered_date=delivery_date, expiration_date=expiration_date, user_id=user_id)


        stocks.save()

        if stocks.id:
            system_config = SystemConfiguration.objects.first()
            system_config.inventory_code = code
            system_config.save()

        return JsonResponse({'data': 'success'})
    
def received_item_load(request):
    dateToday = date.today()

    stock_data = Stocks.objects.select_related().filter(created_at__date=dateToday)
    total = stock_data.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        stock_data = stock_data[start:start + length]

    data = []

    for stock in stock_data:
        userData = AuthUser.objects.filter(id=stock.user.id)
        itemData = Items.objects.select_related().filter(id=stock.item.id)

        full_name = userData[0].first_name + ' ' + userData[0].last_name
        item_details = itemData[0].generic.name + ' ' + itemData[0].sub_generic.name + ' ' + itemData[0].classification + ' ' + itemData[0].description

        stock_item = {
            'id': stock.id,
            'item_type': itemData[0].type.name,
            'quantity': stock.pcs_quantity,
            'details': item_details,
            'unit_price': stock.unit_price,
            'retail_price': stock.retail_price,
            'expiration_date': stock.expiration_date,
            'delivered_date': stock.delivered_date,
            'created_at': stock.created_at,
            'updated_at': stock.updated_at,
            'created_by': full_name
        }

        data.append(stock_item)

    response = {
        'data': data,
        'page': page,
        'per_page': per_page,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)
