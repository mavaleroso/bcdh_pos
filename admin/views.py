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
from django.db.models import Max
from django.utils import timezone



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
    try:
        user_name = request.POST.get('Username')
        firstname = request.POST.get('Firstname')
        middlename = request.POST.get('Middlename')
        lastname = request.POST.get('Lastname')
        password = request.POST.get('Password')
        email = request.POST.get('Email')
        role_id = request.POST.get('Roles')
        birth_date = request.POST.get('Birthdate')
        sex = request.POST.get('Sex')
        address = request.POST.get('Address')
        position = request.POST.get('Position')
        password = make_password(password)
        user_id = request.session.get('user_id', 0)

        if AuthUser.objects.filter(username=user_name):
            return JsonResponse({'data': 'error', 'message': 'Username Taken'})
        
        else:
            user_add = AuthUser(password = password,is_superuser=role_id,username=user_name,first_name=firstname,last_name=lastname,email=email,date_joined=timezone.now())
            user_add.save()

            max_id = AuthUser.objects.aggregate(max_id=Max('id'))['max_id']
            user_details_add = UserDetails(middle_name=middlename, birthdate=birth_date, sex=sex,address=address,position=position,role_id = role_id,user_id = max_id, added_by_user_id = user_id)
            user_details_add.save()

            return JsonResponse({'data': 'success'})
    except Exception as e:
        return JsonResponse({'data': 'error'})
    
#End User function ---------------->


@csrf_exempt
def user_update(request):
    try:
        id = request.POST.get('ModalID')
        user_name = request.POST.get('ModalUsername')
        firstname = request.POST.get('ModalFname')
        middlename = request.POST.get('ModalMname')
        lastname = request.POST.get('ModalLname')
        email = request.POST.get('ModalEmail')
        birth_date = request.POST.get('ModalBirthdate')
        sex = request.POST.get('ModalSex')
        address = request.POST.get('ModalAddress')
        position = request.POST.get('ModalPosition')
        user_id = request.session.get('user_id', 0)
        status = request.POST.get('ModalStatus')
        if AuthUser.objects.filter(username=user_name).exclude(id=id):
            return JsonResponse({'data': 'error', 'message': 'Username Taken'})
        
        else:
            AuthUser.objects.filter(id=id).update(username=user_name,first_name=firstname,last_name=lastname,email=email,is_active = status)
            UserDetails.objects.filter(user_id=id).update(middle_name=middlename, birthdate=birth_date, sex=sex,address=address,position=position)
            return JsonResponse({'data': 'success'})
    except Exception as e:
        return JsonResponse({'data': 'error'})

@csrf_exempt
def user_edit(request):
    id = request.GET.get('id')
    items = AuthUser.objects.get(pk=id)
    userdetail = UserDetails.objects.get(user_id=id)
    data = serialize("json", [items])
    data = json.loads(data)
    userdetail_data = serialize("json", [userdetail])
    userdetail_data = json.loads(userdetail_data)
    data[0]['fields'].update(userdetail_data[0]['fields'])
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def role_edit(request):
    id = request.GET.get('id')
    items = AuthUser.objects.get(pk=id)
    userdetail = UserDetails.objects.get(user_id=id)
    data = serialize("json", [items])
    data = json.loads(data)
    userdetail_data = serialize("json", [userdetail])
    userdetail_data = json.loads(userdetail_data)
    data[0]['fields'].update(userdetail_data[0]['fields'])
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def role_update(request):
    try:
        id = request.POST.get('RoleID')
        role = request.POST.get('ModalRole')
        UserDetails.objects.filter(user_id=id).update(role_id=role)
        return JsonResponse({'data': 'success'})
    except Exception as e:
        return JsonResponse({'data': 'error'})
    
@csrf_exempt
def update_password(request):
    try:
        user_id= request.POST.get('PasswordID')
        password_ = request.POST.get('ModalPassword')
        AuthUser.objects.filter(id=user_id).update(password = make_password(password_))
        return JsonResponse({'data': 'success'})
    except Exception as e:
        return JsonResponse({'data': 'error'})

def user_load(request):    
    user_data = AuthUser.objects.select_related('userdetails').order_by('-date_joined')
    id_list = [item.id for item in user_data]
    total = user_data.count()
    data = []
    user_details = UserDetails.objects.filter(user_id__in=id_list)

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        user_data = user_data[start:start + length]
        
        
    for item in user_data:
        user_details_item = next((detail for detail in user_details if detail.user_id == item.id), None)
        if user_details_item:
            role_name = user_details_item.role.role_name if user_details_item.role else None
            user_data_item = {
                'user_details_id': user_details_item.id,
                'middle_name': user_details_item.middle_name,
                'birthdate': user_details_item.birthdate,
                'sex': user_details_item.sex,
                'address': user_details_item.address,
                'position': user_details_item.position,
                'role_name': role_name,
                'id': item.id,
                'username': item.username,
                'first_name': item.first_name,
                'last_name': item.last_name,
                'email': item.email,
                'is_active': item.is_active,
            }
            data.append(user_data_item)

    response = {
        'data_user': data,
        'data': data,
        'page': page,
        'per_page': per_page,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)
#end ----------->

       
