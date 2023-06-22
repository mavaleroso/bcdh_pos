# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from main.models import (Items, ItemType, Generic, SubGeneric, Brand, AuthUser)
from django.core.serializers import serialize
from django.http import HttpResponse
from django.db import IntegrityError
import math
from django.db.models import Q
from functools import reduce


def item(request):
    context = {
        'item_type': ItemType.objects.filter().order_by('name'),
        'generic': Generic.objects.filter().order_by('name'),
        'sub_generic': SubGeneric.objects.filter().order_by('name'),
        'brand': Brand.objects.filter().order_by('name'),
    }
    return render(request, 'libraries/items.html', context)


@csrf_exempt
def item_add(request):
    barcode = request.POST.get('ItemBarcode')
    description = request.POST.get('Description')
    classification = request.POST.get('Classification')
    generic_id = request.POST.get('Generic')
    sub_generic_id = request.POST.get('SubGeneric')
    brand_id = request.POST.get('Brand')
    type_id = request.POST.get('ItemType')
    user_id = request.session.get('user_id', 0)

    item_add = Items(barcode=barcode, description=description, classification=classification,
                     generic_id=generic_id, sub_generic_id=sub_generic_id, brand_id=brand_id, type_id=type_id, user_id=user_id)

    try:
        item_add.save()
        return JsonResponse({'data': 'success'})
    except IntegrityError as e:
        if 1062 in e.args:
            return JsonResponse({'data': 'error', 'message': 'Duplicate Barcode'})
        else:
            return JsonResponse({'data': 'error', 'message': 'Data Error'})


@csrf_exempt
def item_update(request):
    id = request.POST.get('ItemID')
    barcode = request.POST.get('ItemBarcode')
    description = request.POST.get('Description')
    classification = request.POST.get('Classification')
    generic_id = request.POST.get('Generic')
    sub_generic_id = request.POST.get('SubGeneric')
    brand_id = request.POST.get('Brand')
    type_id = request.POST.get('ItemType')

    check_barcode = False
    if Items.objects.filter(barcode=barcode).exclude(id=id):
        return JsonResponse({'data': 'error', 'message': 'Duplicate Barcode'})
    else:
        check_barcode = True
    if check_barcode:
        Items.objects.filter(id=id).update(barcode=barcode, description=description, classification=classification,
                                           generic_id=generic_id, sub_generic_id=sub_generic_id, brand_id=brand_id, type_id=type_id)
        return JsonResponse({'data': 'success'})


def item_edit(request):
    id = request.GET.get('id')
    items = Items.objects.get(pk=id)
    data = serialize("json", [items])
    return HttpResponse(data, content_type="application/json")


def item_load(request):
    item_data = Items.objects.select_related().order_by('-created_at').reverse()
    total = item_data.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        item_data = item_data[start:start + length]

    data = []

    for item in item_data:
        userData = AuthUser.objects.filter(id=item.user.id)
        full_name = userData[0].first_name + ' ' + userData[0].last_name

        item = {
            'id': item.id,
            'barcode': item.barcode,
            'item_type': item.type.name,
            'generic': item.generic.name,
            'sub_generic': item.sub_generic.name,
            'classification': item.classification,
            'description': item.description,
            'brand': item.brand.name if item.brand_id is not None else '',
            'created_at': item.created_at,
            'updated_at': item.updated_at,
            'created_by': full_name
        }

        data.append(item)

    response = {
        'data': data,
        'page': page,
        'per_page': per_page,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


def item_collections(request):
    filter = request.GET.get('q')
    data = []
    item_data = Items.objects.select_related()

    for item in item_data:

        item_desc = '['+item.barcode+'] ' + item.generic.name + ' ' + \
            item.sub_generic.name + ' ' + item.classification + ' ' + item.description

        if (filter in item_desc):
            data.append({'item_id': item.id, 'barcode': item.barcode,
                         'item_type': item.type.name, 'brand': item.brand.name, 'item_desc': item_desc})

    return JsonResponse(data, safe=False)


def fetch_item_by_barcode(request):
    barcode = request.GET.get('barcode', '')
    item_data = Items.objects.select_related().filter(barcode=barcode)

    if item_data:
        item_data = item_data[0]

        item = {
            'id': item_data.id,
            'barcode': item_data.barcode,
            'item_type': item_data.type.name,
            'brand': item_data.brand.name if item_data.brand_id is not None else '',
            'details': item_data.generic.name + ' ' + item_data.sub_generic.name + ' ' + item_data.classification + ' ' + item_data.description,
        }

        response = {
            'status': 'success',
            'data': item,
        }
    else:
        response = {
            'status': 'error',
            'message': 'no data found',
        }

    return JsonResponse(response)
