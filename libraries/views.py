# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from libraries.models import (Items)
from main.models import (ItemType, Generic, SubGeneric, Brand, AuthUser)
import math


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
    barcode = request.POST.get('ItemBarcode');
    description = request.POST.get('Description');
    classification = request.POST.get('Classification');
    generic_id = request.POST.get('Generic');
    sub_generic_id = request.POST.get('SubGeneric');
    brand_id = request.POST.get('Brand');
    type_id = request.POST.get('ItemType');
    user_id = request.session.get('user_id', 0)
    
    item_add = Items(barcode=barcode, description=description, classification=classification, generic_id=generic_id, sub_generic_id=sub_generic_id, brand_id=brand_id, type_id=type_id, user_id=user_id)

    item_add.save()

    return JsonResponse({'data': 'success'})

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

