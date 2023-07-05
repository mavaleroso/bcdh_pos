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

       
