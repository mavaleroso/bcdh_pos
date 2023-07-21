# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from main.models import (Items, ItemType, Company, Generic, SubGeneric,
                         Brand, Unit, AuthUser, UserDetails, Clients, ClientType, RoleDetails)
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.serializers import serialize
from django.http import HttpResponse
from django.db import IntegrityError
import math
from django.db.models import Q
from functools import reduce
from django.core import serializers


def get_user_details(request):
    return UserDetails.objects.filter(user_id=request.user.id).first()


def item(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'item_type': ItemType.objects.filter().order_by('name'),
        'generic': Generic.objects.filter().order_by('name'),
        'sub_generic': SubGeneric.objects.filter().order_by('name'),
        'brand': Brand.objects.filter().order_by('name'),
        'role_permission': role.role_name,
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

        brand_name = item.brand.name if item.brand else ''

        if (filter in item_desc):
            data.append({'item_id': item.id, 'barcode': item.barcode,
                        'item_type': item.type.name, 'brand': brand_name, 'item_desc': item_desc})

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


# starts Company function ---------------->

@login_required(login_url='login')
def company(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'company': Company.objects.filter().order_by('name'),
        'role_permission': role.role_name,
    }
    return render(request, 'libraries/company.html', context)


@csrf_exempt
def company_add(request):
    company_ = request.POST.get('Company')
    code_ = request.POST.get('Code')
    address_ = request.POST.get('Address')
    remarks_ = request.POST.get('Remarks')
    user_id = request.session.get('user_id', 0)
    company_add = Company(name=company_, code=code_,
                          address=address_, remarks=remarks_)
    try:
        company_add.save()
        return JsonResponse({'data': 'success'})
    except IntegrityError as e:
        return JsonResponse({'data': 'error'})


@csrf_exempt
def company_update(request):
    id = request.POST.get('ItemID')
    company_ = request.POST.get('Company')
    code_ = request.POST.get('Code')
    address_ = request.POST.get('Address')
    remarks_ = request.POST.get('Remarks')
    status = request.POST.get('Status')

    if Company.objects.filter(name=company_).exclude(id=id):
        return JsonResponse({'data': 'error', 'message': 'Duplicate Company'})
    else:
        Company.objects.filter(id=id).update(
            name=company_, code=code_, address=address_, remarks=remarks_, is_active=status)
        return JsonResponse({'data': 'success'})


def company_edit(request):
    id = request.GET.get('id')
    items = Company.objects.get(pk=id)
    data = serialize("json", [items])
    return HttpResponse(data, content_type="application/json")


def company_load(request):
    company_data = Company.objects.select_related().order_by('-created_at').reverse()
    total = company_data.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        company_data = company_data[start:start + length]

    data = []

    for item in company_data:
        item = {
            'id': item.id,
            'name': item.name,
            'code': item.code,
            'address': item.address,
            'remarks': item.remarks,
            'created_at': item.created_at,
            'status': item.is_active

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
# end ----------->

# starts Brand function ---------------->


@login_required(login_url='login')
def brand(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'brand': Brand.objects.filter().order_by('name'),
        'role_permission': role.role_name,
    }
    return render(request, 'libraries/brand.html', context)


@csrf_exempt
def brand_add(request):
    brand = request.POST.get('Brand')
    brand_add = Brand(name=brand)
    try:
        brand_add.save()
        return JsonResponse({'data': 'success'})
    except IntegrityError as e:
        return JsonResponse({'data': 'error'})


@csrf_exempt
def brand_update(request):
    id = request.POST.get('ItemID')
    brand_ = request.POST.get('Brand')
    status = request.POST.get('Status')

    if Brand.objects.filter(name=brand_).exclude(id=id):
        return JsonResponse({'data': 'error', 'message': 'Duplicate Brand'})
    else:
        Brand.objects.filter(id=id).update(name=brand_, is_active=status)
        return JsonResponse({'data': 'success'})


def brand_edit(request):
    id = request.GET.get('id')
    items = Brand.objects.get(pk=id)
    data = serialize("json", [items])
    return HttpResponse(data, content_type="application/json")


def brand_load(request):
    brand_data = Brand.objects.select_related().order_by('-created_at').reverse()
    total = brand_data.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        brand_data = brand_data[start:start + length]

    data = []

    for item in brand_data:
        item = {
            'id': item.id,
            'name': item.name,
            'status': item.is_active,
            'created_at': item.created_at

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
# end ----------->

# starts Generic function ---------------->


@login_required(login_url='login')
def generic(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'generic': Generic.objects.filter().order_by('name'),
        'role_permission': role.role_name,
    }
    return render(request, 'libraries/generic.html', context)


@csrf_exempt
def generic_add(request):
    generic = request.POST.get('Generic')
    generic_add = Generic(name=generic)
    try:
        generic_add.save()
        return JsonResponse({'data': 'success'})
    except IntegrityError as e:
        return JsonResponse({'data': 'error'})


@csrf_exempt
def generic_update(request):
    id = request.POST.get('ItemID')
    generic_ = request.POST.get('Generic')
    status = request.POST.get('Status')

    if Generic.objects.filter(name=generic_).exclude(id=id):
        return JsonResponse({'data': 'error', 'message': 'Duplicate Generic'})
    else:
        Generic.objects.filter(id=id).update(name=generic_, is_active=status)
        return JsonResponse({'data': 'success'})


def generic_edit(request):
    id = request.GET.get('id')
    items = Generic.objects.get(pk=id)
    data = serialize("json", [items])
    return HttpResponse(data, content_type="application/json")


def generic_load(request):
    generic_data = Generic.objects.select_related().order_by('-created_at').reverse()
    total = generic_data.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        generic_data = generic_data[start:start + length]

    data = []

    for item in generic_data:
        item = {
            'id': item.id,
            'name': item.name,
            'status': item.is_active,
            'created_at': item.created_at

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
# end ----------->


@login_required(login_url='login')
def subgeneric(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()

    context = {
        'sub_generic': SubGeneric.objects.filter().order_by('name').select_related(),
        'generic': Generic.objects.filter(),
        'role_permission': role.role_name,
    }
    return render(request, 'libraries/sub_generic.html', context)


@csrf_exempt
def addsubgeneric(request):
    if request.method == 'POST':
        subgeneric_name = request.POST.get('subgenericname')
        generic_id = request.POST.get('generic_id')

        if SubGeneric.objects.filter(name=subgeneric_name):
            return JsonResponse({'data': 'error'})
        else:
            check_subgeneric = True
        if check_subgeneric:
            add = SubGeneric(
                name=subgeneric_name, generic_id=generic_id)
            add.save()
            return JsonResponse({'data': 'success'})


@csrf_exempt
def updatesubgeneric(request):
    if request.method == 'POST':
        subgeneric_id = request.POST.get('subgeneric_id')
        subgeneric_name = request.POST.get('subgenericname')
        gen_id = request.POST.get('generic_id')
        status = request.POST.get('is_active')

        print("testko")
        print(subgeneric_id)
        print(subgeneric_name)
        print(gen_id)
        print(status)

        check_subgeneric = False
        if SubGeneric.objects.filter(name=subgeneric_name).exclude(id=subgeneric_id):
            return JsonResponse({'data': 'error'})
        else:
            check_subgeneric = True
        if check_subgeneric:
            SubGeneric.objects.filter(id=subgeneric_id).update(
                name=subgeneric_name, generic_id=gen_id, is_active=status)
            return JsonResponse({'data': 'success'})


@login_required(login_url='login')
def units(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'units': Unit.objects.filter().order_by('name'),
        'role_permission': role.role_name,
    }
    return render(request, 'libraries/units.html', context)


@csrf_exempt
def addunits(request):
    if request.method == 'POST':
        check_units = False
        units_name = request.POST.get('unitsname')
        if Units.objects.filter(name=units_name):
            return JsonResponse({'data': 'error'})
        else:
            check_units = True
        if check_units:
            add = Units(
                name=units_name)
            add.save()
            return JsonResponse({'data': 'success'})


@csrf_exempt
def updateunits(request):
    if request.method == 'POST':
        units_id = request.POST.get('units_id')
        units_name = request.POST.get('unitsname')
        status = request.POST.get('is_active')

        check_units = False
        units_name = request.POST.get('unitsname')
        if Units.objects.filter(name=units_name).exclude(id=units_id):
            return JsonResponse({'data': 'error'})
        else:
            check_units = True
        if check_units:
            Units.objects.filter(id=units_id).update(
                name=units_name, is_active=status)
            return JsonResponse({'data': 'success'})


def clients_collections(request):
    filter = request.GET.get('q')
    data = []
    clients_data = Clients.objects.select_related().filter(client_type_id=3)

    for cd in clients_data:

        client_description = cd.first_name + ' ' + \
            cd.middle_name + ' ' + cd.last_name

        if (filter.lower() in client_description.lower()):
            data.append(
                {'item_id': cd.id, 'item_desc': client_description})

    return JsonResponse(data, safe=False)


def get_client(request):
    client_id = request.GET.get('id')
    client_data = Clients.objects.filter(id=client_id).values()

    return JsonResponse(list(client_data), safe=False)
