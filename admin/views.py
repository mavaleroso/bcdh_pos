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
    print("test")
    print(context)
    return render(request, 'admin/company.html', context)

def generic(request):
    context = {
		'generic' : Generic.objects.filter().order_by('name'),
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
    add = Generic(
          name=request.POST.get('genericname'))
    add.save()
    return JsonResponse({'data': 'success'})


