from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import ( ItemType, Company, Generic, SubGeneric, Brand, Unit, AuthUser, UserDetails )
import json 
from django.core import serializers
import datetime
from django.contrib.auth.hashers import make_password


def brand(request):
    context = {
		'brand' : Brand.objects.filter().order_by('name'),
	}
    return render(request, 'admin/brand.html', context)

def company(request):
    qs_json = serializers.serialize('json', Company.objects.filter().order_by('name'))
    contextold = {
		'company' : qs_json,
	}
    context = {
		'company' : Company.objects.filter().order_by('name'),
	}
    return render(request, 'admin/company.html', context)

def generic(request):
    context = {
        'generic' : Generic.objects.filter().order_by('id'),
	}
    return render(request, 'admin/generic.html', context)

def subgeneric(request):
    context = {
		'sub_generic' : SubGeneric.objects.filter().order_by('name'),
	}
    return render(request, 'admin/sub_generic.html', context)

def user(request):
    context = {
		'users' : AuthUser.objects.filter().exclude(id=1).order_by('first_name').select_related('userdetails')
	}
    return render(request, 'admin/users.html', context)

@csrf_exempt
def addgeneric(request):
    if request.method == 'POST':
        print("addni")
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
        birth_date = request.POST.get('birthdate')
        address_ = request.POST.get('address')
        sex_ = request.POST.get('sex')
        position_ = request.POST.get('position')

        print("testing")
        print(password_)

        if AuthUser.objects.filter(username=username_):
            print("halasaroles")
            return JsonResponse({'data': 'error'})
        else:
            add_authuser = AuthUser(
                password = make_password(password_),is_superuser = roles ,username= username_, first_name = firstname, last_name = lastname, email = email_, date_joined = datetime.datetime.now())
            add_authuser.save()
            
            add_user_details = UserDetails(
                middle_name = middle_name_ ,birthdate= birth_date, sex = sex_, address = address_, position = position_, user_id = AuthUser.objects.last().id)
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
        birth_date = request.POST.get('birthdate')
        address_ = request.POST.get('address')
        sex_ = request.POST.get('sex')
        position_ = request.POST.get('position')
        status = request.POST.get('is_active')

        if AuthUser.objects.filter(username=username_).exclude(id=user_id_):
            return JsonResponse({'data': 'error'})
        
        else:
            AuthUser.objects.filter(id=user_id_).update(password = make_password(password_),is_superuser = roles,username=username_,first_name=firstname,last_name=lastname, email = email_, is_active = status)
            UserDetails.objects.filter(user_id=user_id_).update(middle_name=middle_name_,birthdate=birth_date,sex=sex_, address = address_, position = position_)
            return JsonResponse({'data': 'success'})
        



