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
from main.models import ( ItemType, Company, Generic, SubGeneric, Brand, Unit )
import json 
from django.core import serializers


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
		'sub_generic' : SubGeneric.objects.filter().order_by('name'),
	}
    return render(request, 'admin/sub_generic.html', context)

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
        



