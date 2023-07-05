# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import ( ItemType, Company, Generic, SubGeneric, Brand, Unit, AuthUser, UserDetails, Clients, ClientType, RoleDetails )
import json 
from django.core import serializers
import datetime
from django.contrib.auth.hashers import make_password



def is_member_of_inventory_staff(user):
    return user.groups.filter(name='inventory_staff').exists()


def get_user_details(request):
    return UserDetails.objects.filter(user_id=request.user.id).first()

@login_required(login_url='login')
# @role_required(allowed_roles=["admin"])
def brand(request):
    context = {
		'brand' : Brand.objects.filter().order_by('name'),
	}
    return render(request, 'admin/brand.html', context)

@login_required(login_url='login')
def company(request):
    if request.role =="Admin":
        qs_json = serializers.serialize('json', Company.objects.filter().order_by('name'))
        contextold = {
            'company' : qs_json,
        }
        context = {
            'company' : Company.objects.filter().order_by('name'),
        }
        return render(request, 'admin/company.html', context)
        


@login_required(login_url='login')
def generic(request):
    user_details = get_user_details(request)
    allowed_roles = ["Admin", "Management"] 
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    if role.role_name in allowed_roles:
        context = {
            'generic' : Generic.objects.filter().order_by('id'),
            'user_role' : role.role_name,
        }
        return render(request, 'admin/generic.html', context)
    else:
        return render(request, 'pages/unauthorized.html')
        

@login_required(login_url='login')
def subgeneric(request):
    context = {
		'sub_generic' : SubGeneric.objects.filter().order_by('name').select_related(),
        'generic' : Generic.objects.filter()
	}
    return render(request, 'admin/sub_generic.html', context)

@login_required(login_url='login')
def units(request):
    context = {
		'units' : Unit.objects.filter().order_by('name'),
	}
    return render(request, 'admin/units.html', context)

@login_required(login_url='login')
def user(request):
    context = {
		'users' : AuthUser.objects.filter().exclude(id=1).order_by('first_name').select_related('userdetails')
	}
    return render(request, 'admin/users.html', context)

@login_required(login_url='login')
def clients(request):
    context = {
		'clients' : Clients.objects.filter().exclude(id=1).order_by('first_name').select_related(),
        'client_type' : ClientType.objects.filter()
        
	}
    return render(request, 'admin/clients.html', context)


@csrf_exempt
def addgeneric(request):
    if request.method == 'POST':
        check_generic = False
        generic_name = request.POST.get('genericname')
        if Generic.objects.filter(name=generic_name):
            return JsonResponse({'data': 'error'})
        else:
            check_generic = True        
        if check_generic:
            add = Generic(
                name= generic_name)
            add.save()
            return JsonResponse({'data': 'success'})
        
@csrf_exempt
def updategeneric(request):
    if request.method == 'POST':
        generic_id = request.POST.get('generic_id')
        generic_name = request.POST.get('genericname')
        status = request.POST.get('is_active')

        check_generic = False
        generic_name = request.POST.get('genericname')
        if Generic.objects.filter(name=generic_name).exclude(id=generic_id):
            return JsonResponse({'data': 'error'})
        else:
            check_generic = True        
        if check_generic:
            Generic.objects.filter(id=generic_id).update(name=generic_name, is_active=status)
            return JsonResponse({'data': 'success'})

@csrf_exempt
def addbrand(request):
    if request.method == 'POST':
        check_brand = False
        brand_name = request.POST.get('brandname')
        if Brand.objects.filter(name=brand_name):
            return JsonResponse({'data': 'error'})
        else:
            check_brand = True        
        if check_brand:
            add = Brand(
                name= brand_name)
            add.save()
            return JsonResponse({'data': 'success'})
        
@csrf_exempt
def addcompany(request):
    if request.method == 'POST':
        check_generic = False
        generic_name = request.POST.get('companyname')
        code_name = request.POST.get('code')
        address_ = request.POST.get('address')
        remarks = request.POST.get('remarks')
        if Company.objects.filter(name=generic_name):
            return JsonResponse({'data': 'error'})
        else:
            check_generic = True        
        if check_generic:
            add = Company(
                name= generic_name, code = code_name, address = address_, remarks = remarks)
            add.save()
            return JsonResponse({'data': 'success'})
        
@csrf_exempt
def updatecompany(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        company_name = request.POST.get('companyname')
        status = request.POST.get('is_active')
        code_name = request.POST.get('code')
        address_ = request.POST.get('address')
        remarks = request.POST.get('remarks')

        check_company = False
        if Company.objects.filter(name=company_name).exclude(id=company_id):
            return JsonResponse({'data': 'error'})
        else:
            check_company = True        
        if check_company:
            Company.objects.filter(id=company_id).update(name=company_name, is_active=status,code = code_name, address = address_, remarks = remarks)
            return JsonResponse({'data': 'success'})
        

@csrf_exempt
def adduser(request):
    if request.method == 'POST':
        
        firstname = request.POST.get('firstname')
        middle_name_ = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')
        email_ = request.POST.get('username')
        roles = request.POST.get('roles')
        birthdate = request.POST.get('birthdate')
        address_ = request.POST.get('address')
        sex_ = request.POST.get('sex')
        position_ = request.POST.get('position')
        

        if AuthUser.objects.filter(username=username_):
            return JsonResponse({'data': 'error'})
        else:
            add_authuser = AuthUser(
                password = make_password(password_),is_superuser = roles ,username= username_, first_name = firstname, last_name = lastname, email = email_, date_joined = datetime.datetime.now())
            add_authuser.save()
            
            add_user_details = UserDetails(
                middle_name = middle_name_ ,birthdate= birthdate, sex = sex_, address = address_, position = position_, user_id = AuthUser.objects.last().id)
            add_user_details.save()

            return JsonResponse({'data': 'success'})
        
@csrf_exempt
def updateuser(request):
    if request.method == 'POST':
      
        user_id_ = request.POST.get('user_id')
        firstname = request.POST.get('firstname')
        middle_name_ = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        username_ = request.POST.get('username')
        password_ = request.POST.get('password')
        email_ = request.POST.get('email')
        roles = request.POST.get('roles')
        birthdate = request.POST.get('birthdate')
        address_ = request.POST.get('address')
        sex_ = request.POST.get('sex')
        position_ = request.POST.get('position')
        status = request.POST.get('is_active')


        if AuthUser.objects.filter(username=username_).exclude(id=user_id_):
            return JsonResponse({'data': 'error'})
        
        else:
            AuthUser.objects.filter(id=user_id_).update(password = make_password(password_),is_superuser = roles,username=username_,first_name=firstname,last_name=lastname, email = email_, is_active = status)
            UserDetails.objects.filter(user_id=user_id_).update(middle_name=middle_name_,birthdate=birthdate,sex=sex_, address = address_, position = position_)
            return JsonResponse({'data': 'success'})
        

@csrf_exempt
def updatebrand(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
        brand_name = request.POST.get('brandname')
        status = request.POST.get('is_active')

        check_brand = False
        brand_name = request.POST.get('brandname')
        if Brand.objects.filter(name=brand_name).exclude(id=brand_id):
            return JsonResponse({'data': 'error'})
        else:
            check_brand = True        
        if check_brand:
            Brand.objects.filter(id=brand_id).update(name=brand_name, is_active=status)
            return JsonResponse({'data': 'success'})

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
                name= subgeneric_name, generic_id =generic_id )
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
            SubGeneric.objects.filter(id=subgeneric_id).update(name=subgeneric_name, generic_id=gen_id,is_active=status)
            return JsonResponse({'data': 'success'})

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
                name= units_name)
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
            Units.objects.filter(id=units_id).update(name=units_name, is_active=status)
            return JsonResponse({'data': 'success'})

@csrf_exempt
def addclients(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        birthdate = request.POST.get('birthdate')
        sex = request.POST.get('sex')
        address = request.POST.get('address')
        occupation = request.POST.get('occupation')
        client_type = request.POST.get('client_type_id')
        
        add = Clients(
            first_name= first_name, middle_name = middle_name, last_name = last_name, birthdate = birthdate, sex = sex, address = address, client_type_id = client_type)
        add.save()
        return JsonResponse({'data': 'success'})
        
@csrf_exempt
def updateclients(request):
    if request.method == 'POST':
        clients_id = request.POST.get('clients_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        birthdate = request.POST.get('birthdate')
        sex = request.POST.get('sex')
        address = request.POST.get('address')
        occupation = request.POST.get('occupation')
        client_type = request.POST.get('client_type_id')

        Clients.objects.filter(id=clients_id).update(first_name=first_name, middle_name = middle_name, last_name = last_name, birthdate = birthdate, sex = sex, address = address, occupation = occupation, client_type_id = client_type)
        return JsonResponse({'data': 'success'})

       
