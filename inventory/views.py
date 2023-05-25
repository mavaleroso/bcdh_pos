from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from main.models import (Stocks, Items, ItemLocation, SystemConfiguration,
                         ItemType, Company, Generic, SubGeneric, Brand, AuthUser, OutItems, Location)
from datetime import date, datetime
import math
from django.db.models import Q


def inventory_in(request):
    context = {
        'item_type': ItemType.objects.filter().order_by('name'),
        'company': Company.objects.filter().order_by('name'),
        'generic': Generic.objects.filter().order_by('name'),
        'sub_generic': SubGeneric.objects.filter().order_by('name'),
        'brand': Brand.objects.filter().order_by('name'),
    }
    return render(request, 'inventory/in.html', context)


def inventory_list(request):
    context = {
        'item_type': ItemType.objects.filter().order_by('name'),
        'company': Company.objects.filter().order_by('name'),
        'generic': Generic.objects.filter().order_by('name'),
        'sub_generic': SubGeneric.objects.filter().order_by('name'),
        'brand': Brand.objects.filter().order_by('name'),
        'company': Company.objects.filter().order_by('name'),
        'inventory_code': Stocks.objects.filter().order_by('code'),
        'barcode': Items.objects.filter().order_by('barcode'),
        'location': Location.objects.filter().order_by('name'),
    }
    return render(request, 'inventory/list.html', context)


def get_stock_id_availability(stock_data=[], return_val='', availability=False):
    stock_id = []
    for stock in stock_data:
        outItemsData = OutItems.objects.filter(stock_id=stock.id)
        expended_stock = 0
        damage_stock = stock.is_damaged if stock.is_damaged else 0

        for outItem in outItemsData:
            expended_stock = expended_stock + outItem.quantity

        available = stock.pcs_quantity - expended_stock - damage_stock

        if availability == True and available > 0:
            stock_id.append(stock.id)

        elif availability == False and available <= 0:
            stock_id.append(stock.id)

    if return_val == 'stock_id':
        return stock_id


def inventory_load(request):

    _inventory_code_filter = request.GET.getlist(
        'inventory_code_filter[]') if request.GET.getlist('inventory_code_filter[]') else []
    _barcode_filter = request.GET.getlist(
        'barcode_filter[]') if request.GET.getlist('barcode_filter[]') else []
    _item_type_filter = request.GET.getlist(
        'item_type_filter[]') if request.GET.getlist('item_type_filter[]') else []
    _generic_filter = request.GET.getlist(
        'generic_filter[]') if request.GET.getlist('generic_filter[]') else []
    _subgeneric_filter = request.GET.getlist(
        'subgeneric_filter[]') if request.GET.getlist('subgeneric_filter[]') else []
    _classification_filter = request.GET.get('classification_filter')
    _description_filter = request.GET.get('description_filter')
    _brand_filter = request.GET.getlist(
        'brand_filter[]') if request.GET.getlist('brand_filter[]') else []
    _company_filter = request.GET.getlist(
        'company_filter[]') if request.GET.getlist('company_filter[]') else []
    _location_filter = request.GET.getlist(
        'location_filter[]') if request.GET.getlist('location_filter[]') else []
    _is_damage_filter = request.GET.get('is_damage_filter')
    _is_available_filter = request.GET.get('is_available_filter')
    _is_expired_filter = request.GET.get('is_expired_filter')
    _expiration_date_filter = request.GET.get('expiration_date_filter')
    _delivered_date_filter = request.GET.get('delivered_date_filter')

    _search = request.GET.get('search[value]')
    _start = request.GET.get('start')
    _length = request.GET.get('length')
    _order_col_num = request.GET.get('order[0][column]')
    _order_dir = request.GET.get('order[0][dir]')

    def _order_col():
        prefix_col = ''
        column = request.GET.get('columns['+_order_col_num+'][data]')

        if column == 'barcode':
            prefix_col = 'item__' + column
        elif column == 'brand':
            prefix_col = 'item__' + column + '__name'
        elif column == 'company':
            prefix_col = column + '__name'
        else:
            prefix_col = column

        return prefix_col

    _order_dash = '-' if _order_dir == 'desc' else ''

    filters = {}

    if len(_inventory_code_filter) > 0:
        filters['code__in'] = _inventory_code_filter

    if len(_barcode_filter) > 0:
        filters['item__barcode__in'] = _barcode_filter

    if len(_item_type_filter) > 0:
        filters['item__type_id__in'] = _item_type_filter

    if len(_generic_filter) > 0:
        filters['item__generic_id__in'] = _generic_filter

    if len(_subgeneric_filter) > 0:
        filters['item__sub_generic_id__in'] = _subgeneric_filter

    if len(_brand_filter) > 0:
        filters['item__brand_id__in'] = _brand_filter

    if len(_company_filter) > 0:
        filters['company_id__in'] = _company_filter

    if len(_location_filter) > 0:
        stock_id = ItemLocation.objects.filter(
            location_id__in=_location_filter)
        filters['id__in'] = stock_id

    if _classification_filter:
        filters['item__classification__icontains'] = _classification_filter

    if _description_filter:
        filters['item__description__icontains'] = _description_filter

    if _is_damage_filter == 'yes':
        filters['is_damaged__gt'] = 0
    elif _is_damage_filter == 'no':
        filters['is_damaged__lt'] = 1

    if _is_available_filter == 'yes':
        stock_data = Stocks.objects.select_related()
        stock_id = get_stock_id_availability(stock_data, 'stock_id', True)

        filters['id__in'] = stock_id
    elif _is_available_filter == 'no':
        stock_data = Stocks.objects.select_related()
        stock_id = get_stock_id_availability(stock_data, 'stock_id', False)

        filters['id__in'] = stock_id

    if _is_expired_filter == 'yes':
        stock_data = Stocks.objects.select_related()
        stock_id = []
        for stock in stock_data:
            expiration_aging = stock.expiration_date - datetime.now().date()
            if expiration_aging.days <= 0:
                stock_id.append(stock.id)
        filters['id__in'] = stock_id
    elif _is_expired_filter == 'no':
        stock_data = Stocks.objects.select_related()
        stock_id = []
        for stock in stock_data:
            expiration_aging = stock.expiration_date - datetime.now().date()
            if expiration_aging.days > 0:
                stock_id.append(stock.id)
        filters['id__in'] = stock_id

    if _expiration_date_filter:
        filters['expiration_date'] = _expiration_date_filter

    if _delivered_date_filter:
        filters['delivered_date'] = _delivered_date_filter

    stock_data = Stocks.objects.select_related().filter(**filters).filter(
        Q(code__icontains=_search) |
        Q(item__barcode__icontains=_search) |
        Q(item__type__name__icontains=_search) |
        Q(item__brand__name__icontains=_search) |
        Q(company__name__icontains=_search) |
        Q(item__generic__name__icontains=_search) |
        Q(item__sub_generic__name__icontains=_search) |
        Q(item__classification__icontains=_search) |
        Q(item__description__icontains=_search) |
        Q(pcs_quantity__icontains=_search) |
        Q(is_damaged__icontains=_search) |
        Q(unit_price__icontains=_search) |
        Q(retail_price__icontains=_search) |
        Q(expiration_date__icontains=_search) |
        Q(delivered_date__icontains=_search)
    ).order_by(_order_dash + _order_col())

    total = stock_data.count()

    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        stock_data = stock_data[start:start + length]

    data = []

    for stock in stock_data:
        userData = AuthUser.objects.filter(id=stock.user.id)
        outItemsData = OutItems.objects.filter(stock_id=stock.id)
        itemLocation = ItemLocation.objects.select_related().filter(stock_id=stock.id)
        full_name = userData[0].first_name + ' ' + userData[0].last_name

        location_data = []

        for il in itemLocation:
            il_obj = {
                'name': il.location.name,
                'quantity': il.quantity
            }
            location_data.append(il_obj)

        expended_stock = 0
        damage_stock = stock.is_damaged if stock.is_damaged else 0

        for outItem in outItemsData:
            expended_stock = expended_stock + outItem.quantity

        available = stock.pcs_quantity - expended_stock - damage_stock

        expiration_aging = stock.expiration_date - datetime.now().date()

        stock_obj = {
            'id': stock.id,
            'code': stock.code,
            'barcode': stock.item.barcode,
            'item_type': stock.item.type.name,
            'brand': stock.item.brand.name,
            'company': stock.company.name,
            'location': location_data,
            'details': stock.item.generic.name + ' ' + stock.item.sub_generic.name + ' ' + stock.item.classification + ' ' + stock.item.description,
            'pcs_quantity': stock.pcs_quantity,
            'damage_stock': stock.is_damaged,
            'available_stock': available,
            'unit_price': stock.unit_price,
            'retail_price': stock.retail_price,
            'expiration_date': stock.expiration_date,
            'expiration_aging': expiration_aging.days,
            'delivered_date': stock.delivered_date,
            'created_at': stock.created_at,
            'updated_at': stock.updated_at,
            'created_by': full_name
        }

        data.append(stock_obj)

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

        stocks = Stocks(code=code, item_id=item_id, company_id=company, unit_price=unit_price, pcs_quantity=item_quantity_pcs,
                        retail_price=retail_price, delivered_date=delivery_date, expiration_date=expiration_date, user_id=user_id)

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
        item_details = itemData[0].generic.name + ' ' + itemData[0].sub_generic.name + \
            ' ' + itemData[0].classification + ' ' + itemData[0].description

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


def inventory_list_edit(request, stock_id):
    context = {
        'company': Company.objects.filter().order_by('name'),
        'stock_details': Stocks.objects.select_related().get(pk=stock_id),
        'items': Items.objects.select_related()
    }
    return render(request, 'inventory/list_edit.html', context)


@csrf_exempt
def update_stock(request, stock_id):
    item_id = request.POST.get('ItemID')
    item_quantity_pcs = request.POST.get('ItemQuantityPcs')
    unit_price = request.POST.get('UnitPrice')
    retail_price = request.POST.get('RetailPricePcs')
    company = request.POST.get('Company')
    delivered_date = request.POST.get('DeliveredDate')
    expiration_date = request.POST.get('ExpirationDate')

    stock = Stocks.objects.get(pk=stock_id)
    stock.item_id = item_id
    stock.pcs_quantity = item_quantity_pcs
    stock.unit_price = unit_price
    stock.retail_price = retail_price
    stock.company_id = company
    stock.delivered_date = delivered_date
    stock.expiration_date = expiration_date
    stock.save()

    return JsonResponse({'data': 'success'})


@csrf_exempt
def update_stock_location(request):
    location_stock_id = request.POST.get('LocationStockId')
    location_data_id = request.POST.getlist('LocationDataId[]')
    location_data_qty = request.POST.getlist('LocationDataQty[]')

    new_location_data = zip(location_data_id, location_data_qty)

    for ldi, ldq in new_location_data:
        quantity = ldq if ldq else 0

        if int(quantity) > 0:
            ItemLocation.objects.update_or_create(
                stock_id=location_stock_id, location_id=ldi, defaults={'quantity': quantity})
        else:
            ItemLocation.objects.filter(
                stock_id=location_stock_id, location_id=ldi).delete()

    return JsonResponse({'data': 'success'})


@csrf_exempt
def update_stock_damage(request):
    damage_stock_id = request.POST.get('DamageStockId')
    damage_stock_qty = request.POST.get('DamageStocks')

    stock_data = Stocks.objects.get(id=damage_stock_id)
    stock_data.is_damaged = damage_stock_qty
    stock_data.save()

    return JsonResponse({'data': 'success'})
