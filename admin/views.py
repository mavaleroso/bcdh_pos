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


def brand(request):
    context = {
		'brand' : Brand.objects.filter().order_by('name'),
	}
    return render(request, 'admin/brand.html', context)

def company(request):
    context = {
		'company' : Company.objects.filter().order_by('name'),
	}
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


