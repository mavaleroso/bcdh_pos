import json
from django.db import connection
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from main.models import (Stocks, StocksItems, Items, StockLocation, SystemConfiguration,
                         ItemType, Company, Generic, SubGeneric, Brand, AuthUser, OutItems, Location, UserDetails, RoleDetails, Sales)
from datetime import date, datetime
import math
import xlwt

from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.db.models.functions import Concat


def get_user_details(request):
    return UserDetails.objects.filter(user_id=request.user.id).first()


def stock_item_data(_column_name='id', _order_dir='asc', _where_item_id_val=None, where_in_search=None):
    query = """
        SELECT 
            id, 
            GROUP_CONCAT(primary_id SEPARATOR ',') AS n_id, 
            barcode, 
            item_type_name, 
            item_details, 
            SUM(quantity) AS total_quantity, 
            unit_price,
            DATEDIFF(expiration_date, DATE(now())) AS date_diff,
            expired_count
        FROM (
            SELECT 
                id, 
                primary_id,
                barcode, 
                item_type_name, 
                item_details, 
                quantity,
                unit_price,
                expiration_date,
                DATEDIFF(expiration_date, DATE(now())) AS date_diff,
                '1' AS expired_count
            FROM (
                SELECT
                        DISTINCT si.item_id AS id,
                        si.id AS primary_id,
                        i.barcode,
                        it.name AS item_type_name,
                        CONCAT(g.name,' ',sg.name,' ',i.classification, ' ', i.description) AS item_details,
                        si.pcs_quantity AS quantity,
                        si.unit_price,
                        si.expiration_date
                FROM stock_items AS si
                JOIN stocks AS s ON s.id = si.stock_id
                JOIN items AS i ON i.id = si.item_id
                JOIN item_type AS it ON it.id = i.type_id
                JOIN generic AS g ON g.id = i.generic_id
                JOIN sub_generic AS sg ON sg.id = i.sub_generic_id
                WHERE DATEDIFF(expiration_date, DATE(now())) < 182
                """+('AND si.item_id IN '+where_in_search+'' if where_in_search else '')+"""
                ORDER BY si.expiration_date
            ) AS rs1 
            UNION ALL
            SELECT 
                id, 
                primary_id,
                barcode, 
                item_type_name, 
                item_details, 
                quantity,
                unit_price,
                expiration_date,
                DATEDIFF(expiration_date, DATE(now())) AS date_diff,
                '0' AS expired_count
                FROM (
                    SELECT
                        DISTINCT si.item_id AS id,
                        si.id AS primary_id,
                        i.barcode,
                        it.name AS item_type_name,
                        CONCAT(g.name,' ',sg.name,' ',i.classification, ' ', i.description) AS item_details,
                        si.pcs_quantity AS quantity,
                        si.unit_price,
                        si.expiration_date
                    FROM stock_items AS si
                    JOIN stocks AS s ON s.id = si.stock_id
                    JOIN items AS i ON i.id = si.item_id
                    JOIN item_type AS it ON it.id = i.type_id
                    JOIN generic AS g ON g.id = i.generic_id
                    JOIN sub_generic AS sg ON sg.id = i.sub_generic_id
                    WHERE DATEDIFF(expiration_date, DATE(now())) > 182
                    """+('AND si.item_id IN '+where_in_search+'' if where_in_search else '')+"""
                    ORDER BY s.delivered_date
                ) AS rs2
        ) AS rs
        """+('WHERE rs.id = '+_where_item_id_val+'' if _where_item_id_val else '')+"""
        GROUP BY id
        ORDER BY """+_column_name+""" """+_order_dir+"""
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    keys = ('id', 'n_id', 'barcode', 'item_type_name', 'item_details', 'total_quantity',
            'unit_price', 'date_diff', 'expired_count')

    result_data = [dict(zip(keys, row)) for row in results]

    return result_data


@login_required(login_url='login')
def inventory_in(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'item_type': ItemType.objects.filter().order_by('name'),
            'company': Company.objects.filter().order_by('name'),
            'generic': Generic.objects.filter().order_by('name'),
            'sub_generic': SubGeneric.objects.filter().order_by('name'),
            'brand': Brand.objects.filter().order_by('name'),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/in.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
def out_sales(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/out_sales.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
def out_inpatient(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'sales': Sales.objects.select_related().filter(category='inpatient'),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/out_inpatient.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
def out_inpatient_create(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'location': Location.objects.filter().order_by('id'),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/out_inpatient_create.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
def out_damage(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'sales': Sales.objects.select_related().filter(category='damage'),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/out_damage.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


@login_required(login_url='login')
def out_damage_create(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'location': Location.objects.filter().order_by('id'),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/out_damage_create.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


def inventory_list(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Sales Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'role_permission': role.role_name,
            'location': Location.objects.filter().order_by('id'),
            'po': Stocks.objects.filter().order_by('id'),
        }
        return render(request, 'inventory/list.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


def get_stock_id_availability(stock_data=[], return_val='', availability=False):
    stock_id = []
    for stock in stock_data:
        outItemsData = OutItems.objects.filter(stock_id=stock['id'])
        expended_stock = 0
        damage_stock = stock.is_damaged if stock.is_damaged else 0

        for outItem in outItemsData:
            expended_stock = expended_stock + outItem.quantity

        available = stock.pcs_quantity - expended_stock - damage_stock

        if availability == True and available > 0:
            stock_id.append(stock['id'])

        elif availability == False and available <= 0:
            stock_id.append(stock['id'])

    if return_val == 'stock_id':
        return stock_id


def inventory_load(request):
    if request.method == 'GET':
        _search = request.GET.get('search[value]')
        _start = request.GET.get('start')
        _length = request.GET.get('length')
        _order_col_num = request.GET.get('order[0][column]')
        _order_dir = request.GET.get('order[0][dir]')
        _column_name = request.GET.get('columns['+_order_col_num+'][data]')
        _search_id = []

        stock_data = stock_item_data(_column_name, _order_dir)

        if _search:
            for stock in stock_data:
                if _search.lower() in stock['item_type_name'].lower():
                    if stock['id'] not in _search_id:
                        _search_id.append(stock['id'])

                if _search.lower() in stock['item_details'].lower():
                    if stock['id'] not in _search_id:
                        _search_id.append(stock['id'])

                if _search in str(stock['total_quantity']):
                    if stock['id'] not in _search_id:
                        _search_id.append(stock['id'])

                if _search in str(stock['unit_price']):
                    if stock['id'] not in _search_id:
                        _search_id.append(stock['id'])

            def where_in_search():
                if len(_search_id) == 1:
                    return "("+str(_search_id[0])+")"
                elif len(_search_id) > 0:
                    return str(tuple(_search_id))
                else:
                    return "(0)"

            stock_data = stock_item_data(
                _column_name, _order_dir, None, where_in_search())

        total = sum(1 for result in stock_data)

        if _start and _length:
            start = int(_start)
            length = int(_length)
            page = math.ceil(start / length) + 1
            per_page = length

            stock_data = stock_data[start:start + length]

        data = []

        for stock in stock_data:

            stock_item_id = [int(num) for num in stock['n_id'].split(',')]

            location_data = Location.objects.filter()

            out_total_qty = OutItems.objects.filter(stock_item_id__in=stock_item_id).aggregate(
                total_quantity=Sum('quantity'))['total_quantity']

            out_total_qty = out_total_qty if out_total_qty != '' else 0

            if out_total_qty is not None:
                stock['total_quantity'] -= out_total_qty

            stock_details_data = {
                'id': stock['id'],
                'stock_item_id': stock_item_id[len(stock_item_id)-1],
                'item_type_name': stock['item_type_name'],
                'details': stock['item_details'],
                'pcs_quantity': stock['total_quantity'],
                'unit_price': stock['unit_price'],
                'date_diff': stock['date_diff'],
                'expired_count': stock['expired_count']
            }

            for l in location_data:
                stock_location_data = StockLocation.objects.filter(
                    stock_item_id__in=stock_item_id)
                out_items_location_data = OutItems.objects.filter(
                    stock_item_id__in=stock_item_id)

                stock_details_data[l.name] = 0
                for sld in stock_location_data:
                    if sld.location_id == l.id:
                        stock_details_data[l.name] += sld.quantity

                for oild in out_items_location_data:
                    if oild.location_id == l.id:
                        stock_details_data[l.name] -= oild.quantity

            data.append(stock_details_data)

        response = {
            'data': data,
            'page': page,
            'per_page': per_page,
            'recordsTotal': total,
            'recordsFiltered': total,
        }

        return JsonResponse(response)


def stock_locations(request):
    if request.method == 'GET':
        item_id = request.GET.get('id')

        locations = Location.objects.filter().order_by('id')
        stock_locations = StockLocation.objects.filter(stock_item__item_id=item_id).order_by('stock_item__stock__code').values(
            'id',
            'stock_item__id',
            'stock_item__pcs_quantity',
            'stock_item__stock__code',
            'location__name',
            'quantity'
        )

        data = []

        for sl in stock_locations:
            out_total_qty = OutItems.objects.filter(stock_item_id=sl['stock_item__id']).aggregate(
                total_quantity=Sum('quantity'))['total_quantity']

            out_total_qty = out_total_qty if out_total_qty != '' else 0

            if out_total_qty is not None:
                sl['stock_item__pcs_quantity'] -= out_total_qty

            if len(data) == 0:
                tmp_data = {
                    'stock_item__id': sl['stock_item__id'],
                    'code': sl['stock_item__stock__code'],
                    'stock_item__pcs_quantity': sl['stock_item__pcs_quantity']
                }
                for l in locations:
                    if sl['location__name'] == l.name:
                        tmp_data[l.name] = sl['quantity']
                    else:
                        tmp_data[l.name] = 0

                data.append(tmp_data)
            else:
                if not [item for item in data if item['stock_item__id'] == sl['stock_item__id']]:
                    tmp_data = {
                        'stock_item__id': sl['stock_item__id'],
                        'code': sl['stock_item__stock__code'],
                        'stock_item__pcs_quantity': sl['stock_item__pcs_quantity']
                    }

                    for l in locations:
                        if sl['location__name'] == l.name:
                            tmp_data[l.name] = sl['quantity']
                        else:
                            tmp_data[l.name] = 0

                    data.append(tmp_data)

            for d in data:
                if d['stock_item__id'] == sl['stock_item__id']:
                    for l in locations:
                        if sl['location__name'] == l.name:
                            d[l.name] = sl['quantity']

        for d in data:
            out_items_data = OutItems.objects.filter(stock_item_id=d['stock_item__id']).values(
                'stock_item_id', 'location__name'
            ).annotate(
                total_quantity=Sum('quantity')
            )

            for oid in out_items_data:
                if oid['stock_item_id'] == d['stock_item__id']:
                    for l in locations:
                        if oid['location__name'] == l.name:
                            d[l.name] -= oid['total_quantity']

        response = {
            'data': data,
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
def store_stock_data(request):
    if request.method == 'POST':
        company = request.POST.get('Company')
        delivery_date = request.POST.get('DeliveredDate')
        item_count = request.POST.get('item_count')

        user_id = request.session.get('user_id', 0)
        code = generate_code()

        stocks = Stocks(code=code, company_id=company,
                        delivered_date=delivery_date, user_id=user_id)

        stocks.save()

        if stocks.id:
            system_config = SystemConfiguration.objects.first()
            system_config.inventory_code = code
            system_config.save()

        for i in range(int(item_count)):
            counter = i + 1
            counter = str(counter)
            item_id = request.POST.get('item_id['+counter+']')
            quantity = request.POST.get('quantity['+counter+']')
            unit_price = request.POST.get('unit_price['+counter+']')
            expiration_date = request.POST.get('expiration_date['+counter+']')

            stock_items = StocksItems(stock_id=stocks.id, item_id=item_id, pcs_quantity=quantity,
                                      unit_price=unit_price, expiration_date=expiration_date)

            stock_items.save()

            stock_location = StockLocation(
                quantity=quantity, location_id=1, stock_item_id=stock_items.id)

            stock_location.save()

        return JsonResponse({'data': 'success'})


def update_stock_data(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id')
        company = request.POST.get('Company')
        delivery_date = request.POST.get('DeliveredDate')
        item_count = request.POST.get('item_count')

        user_id = request.session.get('user_id', 0)

        stocks = Stocks.objects.get(pk=stock_id)
        stocks.company_id = company
        stocks.delivery_date = delivery_date
        stocks.user_id = user_id

        stocks.save()

        StocksItems.objects.filter(stock_id=stock_id).delete()

        for i in range(int(item_count)):
            counter = i + 1
            counter = str(counter)
            stock_item_id = request.POST.get('stock_item_id['+counter+']')
            item_id = request.POST.get('item_id['+counter+']')
            quantity = request.POST.get('quantity['+counter+']')
            unit_price = request.POST.get('unit_price['+counter+']')
            expiration_date = request.POST.get('expiration_date['+counter+']')

            if stock_item_id == '0':
                stock_items_1 = StocksItems(stock_id=stocks.id, item_id=item_id, pcs_quantity=quantity,
                                            unit_price=unit_price, expiration_date=expiration_date)
                stock_items_1.save()
            else:
                stock_items_2 = StocksItems(id=stock_item_id, stock_id=stocks.id, item_id=item_id, pcs_quantity=quantity,
                                            unit_price=unit_price, expiration_date=expiration_date)
                stock_items_2.save()

        return JsonResponse({'data': 'success'})


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


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bcdh_inventory_"' + \
        datetime.now().strftime("%m_%d_%Y")+'".xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Code', 'Company', 'Item Description', 'Inventory Evaluation Method', 'Unit Price', 'Retail Price',
               'Quantity in Stocks', 'Unit of Measurement', 'Total Cost', 'Expiration Date', 'Aging', 'Delivery Date', 'Prev. Qty.']

    stock_data = Stocks.objects.all().select_related()

    data = []

    for stock in stock_data:
        outItemsData = OutItems.objects.filter(stock_id=stock['id'])
        stockLocation = StockLocation.objects.select_related().filter(
            stock_id=stock['id'])

        expended_stock = 0
        damage_stock = stock.is_damaged if stock.is_damaged else 0

        for outItem in outItemsData:
            expended_stock = expended_stock + outItem.quantity

        available = stock.pcs_quantity - expended_stock - damage_stock

        expiration_aging = stock.expiration_date - datetime.now().date()

        stock_obj = [
            stock.code,
            stock.company.name,
            stock.item.generic.name + ' ' + stock.item.sub_generic.name +
            ' ' + stock.item.classification + ' ' + stock.item.description,
            'FIFO',
            stock.unit_price,
            stock.retail_price,
            available,
            'PCS',
            stock.unit_price * available,
            stock.expiration_date,
            expiration_aging.days,
            stock.delivered_date,
            stock.pcs_quantity
        ]

        for il in stockLocation:
            columns.append(il.location.name)
            stock_obj.append(il.quantity)

        data.append(stock_obj)

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in data:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


def inventory_po_list(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Sales Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'role_permission': role.role_name
        }
        return render(request, 'inventory/po_list.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


def inventory_po_load(request):
    _search = request.GET.get('search[value]')
    _start = request.GET.get('start')
    _length = request.GET.get('length')
    _order_dir = request.GET.get('order[0][dir]')
    _order_dash = '-' if _order_dir == 'desc' else ''
    _order_col_num = request.GET.get('order[0][column]')

    def _order_col():
        prefix_col = ''
        column = request.GET.get('columns['+_order_col_num+'][data]')

        if column == 'company':
            prefix_col = 'company__' + column
        else:
            prefix_col = column

        return prefix_col

    stock_data = Stocks.objects.select_related().filter(
        Q(code__icontains=_search) |
        Q(company__name__icontains=_search) |
        Q(delivered_date__icontains=_search) |
        Q(user__username__icontains=_search)
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
        stock_obj = {
            'id': stock['id'],
            'code': stock.code,
            'company': stock.company.name,
            'delivered_date': stock.delivered_date,
            'created_by': stock.user.username
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


def po_export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bcdh_inventory_po_"' + \
        datetime.now().strftime("%m_%d_%Y")+'".xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['PO Code', 'Company', 'Delivered Date', 'Created By']

    stock_data = Stocks.objects.all().select_related()

    data = []

    for stock in stock_data:
        stock_obj = [
            stock.code,
            stock.company.name,
            stock.delivered_date,
            stock.user.username
        ]

        data.append(stock_obj)

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in data:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


def po_view(request, stock_id):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'item_type': ItemType.objects.filter().order_by('name'),
            'company': Company.objects.filter().order_by('name'),
            'generic': Generic.objects.filter().order_by('name'),
            'sub_generic': SubGeneric.objects.filter().order_by('name'),
            'brand': Brand.objects.filter().order_by('name'),
            'stock_data': Stocks.objects.select_related().get(id=stock_id),
            'stock_items_data': StocksItems.objects.select_related().filter(stock_id=stock_id),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/po_view.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


def po_delete(request):
    stock_id = request.POST.get('stock_id')
    stock_data = Stocks.objects.get(pk=stock_id)
    stock_data.delete()
    return JsonResponse({'data': 'success'})


def update_stock_locations(request):
    if request.method == 'POST':
        stock_item_id = request.POST.get('po')
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        transfer_quantity = request.POST.get('transfer_quantity')

        stock_location_query = StockLocation.objects.filter(
            stock_item_id=stock_item_id, location_id=to_location)

        if stock_location_query:
            response = stock_location_query.update(
                quantity=stock_location_query[0].quantity +
                int(transfer_quantity),
            )
        else:
            response = stock_location_query.create(
                quantity=int(transfer_quantity),
                location_id=to_location,
                stock_item_id=stock_item_id
            )

        if response:
            stock_location_query_2 = StockLocation.objects.filter(
                stock_item_id=stock_item_id, location_id=from_location)
            stock_location_query_2.update(
                quantity=stock_location_query_2[0].quantity -
                int(transfer_quantity),
            )

        return JsonResponse({'data': 'success'})


def update_inpatient_status(request):
    if request.method == 'POST':
        sales_id = request.POST.get('id')
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')

        Sales.objects.filter(id=sales_id).update(
            status=status, remarks=remarks)

        return JsonResponse({'data': 'success'})


@login_required(login_url='login')
def out_inpatient_edit(request, trans_id):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Inventory Staff", "Admin"]
    if role.role_name in allowed_roles:
        context = {
            'transaction': Sales.objects.select_related().filter(id=trans_id).first(),
            'location': Location.objects.filter().order_by('id'),
            'role_permission': role.role_name,
        }
        return render(request, 'inventory/out_inpatient_edit.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


def inventory_stock_balance(request):
    if request.method == 'GET':
        item_id = request.GET.get('id')

        initial_values_query = """
            SET @run_balqty := 0;
            SET @run_balcost := 0;
            SET @run_baltotal := 0;
        """

        main_query = """
            SELECT 
                rs.* ,
                (CASE
                    WHEN rs.trans_type = 'in' THEN
                        (@run_balqty := @run_balqty + rs.quantity)
                    ELSE
                        (@run_balqty := @run_balqty - rs.quantity)
                END) AS balance_qty,
                (CASE
                    WHEN rs.trans_type = 'in' THEN
                        round( (@run_baltotal := @run_baltotal + rs.total), 2)
                    ELSE
                        round( (@run_baltotal := @run_baltotal - rs.total), 2)
                END) AS balance_total,
                #(CASE
                #    WHEN rs.trans_type = 'in' THEN
                #        round((@run_balcost := @run_baltotal / @run_balqty), 2)
                #    ELSE
                #        round((@run_balcost := @run_baltotal / @run_balqty), 2)
                #END) AS balance_cost
                cost AS balance_cost
            FROM (
                SELECT 
                    s.`code` AS code, 
                    s.delivered_date AS trans_date, 
                    si.id AS trans_id, 
                    si.item_id AS item_id, 
                    si.pcs_quantity AS quantity, 
                    si.unit_price AS cost,
                    (si.unit_price * si.pcs_quantity) AS total,
                    'in' AS trans_type
                FROM stocks AS s
                LEFT JOIN stock_items AS si ON si.stock_id = s.id
                WHERE si.item_id = """+item_id+"""
                UNION ALL 
                SELECT 
                    s2.transaction_code AS code, 
                    s2.created_at as trans_date, 
                    si2.id AS trans_id, 
                    si2.item_id AS item_id, 
                    oi.quantity AS quantity,
                    si2.unit_price AS cost, 
                    (si2.unit_price * oi.quantity) as total,
                    'out' AS trans_type
                FROM sales AS s2
                LEFT JOIN out_items AS oi ON oi.sales_id = s2.id
                LEFT JOIN stock_items AS si2 ON si2.id = oi.stock_item_id
                WHERE si2.item_id = """+item_id+"""
            ) AS rs 
            ORDER BY 
                rs.trans_id, 
                rs.trans_date ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(initial_values_query)
            cursor.execute(main_query)
            data = cursor.fetchall()

        keys = ('code', 'trans_date', 'trans_id', 'item_id', 'quantity', 'cost',
                'total', 'trans_type', 'balance_qty', 'balance_total', 'balance_cost')
        result_data = [dict(zip(keys, row)) for row in data]

        return JsonResponse(result_data, safe=False)


def get_out_items(request):
    if request.method == 'GET':
        trans_id = request.GET.get('trans_id')
        arr_data = []
        out_items_data = OutItems.objects.select_related().filter(
            sales_id=trans_id)
        location_data = Location.objects.filter()

        for oid in out_items_data:
            oid_data = {
                'oid_id': oid.id,
                'id': oid.stock_item.item.id,
                'item': oid.stock_item.item.generic.name + ' ' + oid.stock_item.item.sub_generic.name + ' ' + oid.stock_item.item.classification + ' ' + oid.stock_item.item.description,
                'location_id': oid.location_id,
                'price': oid.stock_item.unit_price,
                'quantity': oid.quantity,
                'stock_item_id': oid.stock_item_id
            }

            stock_data = stock_item_data(
                'id', 'asc', str(oid.stock_item.item.id))

            for stock in stock_data:

                stock_item_id = [int(num) for num in stock['n_id'].split(',')]

                location_data = Location.objects.filter()

                out_total_qty = OutItems.objects.filter(stock_item_id__in=stock_item_id).aggregate(
                    total_quantity=Sum('quantity'))['total_quantity']

                out_total_qty = out_total_qty if out_total_qty != '' else 0

                if out_total_qty is not None:
                    stock['total_quantity'] -= out_total_qty

                for l in location_data:
                    stock_location_data = StockLocation.objects.filter(
                        stock_item_id__in=stock_item_id)
                    out_items_location_data = OutItems.objects.filter(
                        stock_item_id__in=stock_item_id)

                    oid_data[l.name] = 0
                    for sld in stock_location_data:
                        if sld.location_id == l.id:
                            oid_data[l.name] += sld.quantity

                    for oild in out_items_location_data:
                        if oild.location_id == l.id:
                            oid_data[l.name] -= oild.quantity

                    if oid.location_id == l.id:
                        oid_data[l.name] += oid.quantity

            arr_data.append(oid_data)

        return JsonResponse(arr_data, safe=False)


def out_inpatient_update(request):
    if request.method == 'POST':
        trans_id = request.POST.get('trans_id')
        client_id = request.POST.get('cl_id')
        user_id = request.session.get('user_id', 0)
        amt_paid = request.POST.get('amt_paid')
        stock_list = json.loads(request.POST.get('out_stocks'))

        transaction_data = Sales.objects.get(pk=trans_id)

        transaction_data.client_id = client_id
        transaction_data.user_id = user_id
        transaction_data.exact_amount_paid = amt_paid
        transaction_data.save()

        group_id_list = (
            OutItems.objects.filter(sales_id=trans_id)
            .annotate(group_id=Concat('id', Value(''), output_field=CharField()))
            .values_list('group_id', flat=True)
        )

        group_id_list = list(group_id_list)

        for sl in stock_list:
            OutItems.objects.update_or_create(
                stock_item_id=sl['stock_item_id'],
                sales_id=trans_id,
                defaults={"stock_item_id": sl['stock_item_id'], "quantity": sl['qty'],
                          "location_id": sl['location_id'], "discounted_amount": 0, "sales_id": trans_id},
            )

            if sl['oid_id'] != 0:
                group_id_list.remove(str(sl['oid_id']))

        OutItems.objects.filter(id__in=group_id_list).delete()

        return JsonResponse({'data': 'success'})
