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
from main.models import ( ItemType, Generic, SubGeneric, Brand, Unit, AuthUser, UserDetails, Clients, ClientType, RoleDetails )
import json 
from django.core.serializers import serialize
import datetime
from django.contrib.auth.hashers import make_password
import math



def is_member_of_inventory_staff(user):
    return user.groups.filter(name='inventory_staff').exists()

def get_user_details(request):
    return UserDetails.objects.filter(user_id=request.user.id).first()    

@login_required(login_url='login')
def user(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Admin"] 
    if role.role_name in allowed_roles:
        context = {
            'users' : AuthUser.objects.filter().exclude(id=1).order_by('first_name').select_related(),
            'role_permission': role.role_name,
            'role_details': RoleDetails.objects.filter().order_by('role_name'),
        }
        return render(request, 'admin/users.html', context)
    else:
        return render(request, 'pages/unauthorized.html')

@login_required(login_url='login')
def clients(request):
    user_details = get_user_details(request)
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    allowed_roles = ["Admin"] 
    
    if role.role_name in allowed_roles:
        context = {
            'clients' : Clients.objects.filter().exclude(id=1).order_by('first_name').select_related(),
            'client_type' : ClientType.objects.filter(),
            'role_permission': role.role_name,
            
        }
        return render(request, 'admin/clients.html', context)
    else:
        return render(request, 'pages/unauthorized.html')


        

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
        role_id = request.POST.get('roles')
        

        if AuthUser.objects.filter(username=username_):
            return JsonResponse({'data': 'error'})
        else:
            add_authuser = AuthUser(
                password = make_password(password_),is_superuser = roles ,username= username_, first_name = firstname, last_name = lastname, email = email_, date_joined = datetime.datetime.now())
            add_authuser.save()
            
            add_user_details = UserDetails(
                middle_name = middle_name_ ,birthdate= birthdate, sex = sex_, address = address_, position = position_,role_id =role_id , user_id = AuthUser.objects.last().id)
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
            UserDetails.objects.filter(user_id=user_id_).update(middle_name=middle_name_,birthdate=birthdate,sex=sex_, address = address_, position = position_, role_id = roles)
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
    


#start User function ---------------->

@csrf_exempt
def user_add(request):
    user_ = request.POST.get('User')
    code_ = request.POST.get('Code')
    address_ = request.POST.get('Address')
    remarks_ = request.POST.get('Remarks')
    user_id = request.session.get('user_id', 0)
    user_add = AuthUser(name=user_, code=code_, address=address_,remarks=remarks_)
    try:
        user_add.save()
        return JsonResponse({'data': 'success'})
    except Exception as e:
        return JsonResponse({'data': 'error'})
        
@csrf_exempt
def user_update(request):
    id = request.POST.get('ItemID')
    user_ = request.POST.get('User')
    code_ = request.POST.get('Code')
    address_ = request.POST.get('Address')
    remarks_ = request.POST.get('Remarks')
    status = request.POST.get('Status')

    if AuthUser.objects.filter(name=user_).exclude(id=id):
        return JsonResponse({'data': 'error', 'message': 'Duplicate User'})
    else:
        AuthUser.objects.filter(id=id).update(name=user_, code=code_, address=address_,remarks=remarks_,is_active=status)
        return JsonResponse({'data': 'success'})
        

def user_edit(request):
    id = request.GET.get('id')
    items = AuthUser.objects.get(pk=id)
    data = serialize("json", [items])
    return HttpResponse(data, content_type="application/json")

def user_load(request):
    print("Testttttaaa")
    user_data = AuthUser.objects.select_related().order_by('-date_joined').reverse()
    total = user_data.count()
    
    id_list = [user.id for user in user_data]

   
    
    user_details = UserDetails.objects.filter(user_id__in=id_list).select_related()
    
    
    

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        user_data = user_data[start:start + length]
        
        
    data = []

    for item in user_details:
        user_details_item = {
            'user_details_id': item.id,
            'middle_name': item.middle_name,
            'birthdate': item.birthdate,
            'sex': item.sex,
            'address': item.address,
            'position': item.position,
        }
        data.append(user_details_item)

    for item in user_data:
        user_data_item = {
            'id': item.id,
            'username': item.username,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'email': item.email,
            'is_active': item.is_active,
        }
        data.append(user_data_item)
    

    # data = []
    
    # for item in user_details:
    #     item = {
            
    #         'user_details_id': item.id,
    #         'middle_name': item.middle_name,
    #         'birthdate': item.birthdate,
    #         'sex': item.sex,
    #         'address': item.address,
    #         'position': item.position,
    #     }
    #     data.append(item)

    # for item in user_data:
    #     item = {
            
    #         'id': item.id,
    #         'username': item.username,
    #         'first_name': item.first_name,
    #         'last_name': item.last_name,
    #         'email': item.email,
    #         'is_active': item.is_active,


    #     }
    #     data.append(item)
    
    
    

    response = {
        'data': data,
        'page': page,
        'per_page': per_page,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)
#end ----------->

       
