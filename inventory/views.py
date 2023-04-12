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


def inventory_in(request):
    context = {
		'item_type' : ItemType.objects.filter().order_by('name'),
        'company' : Company.objects.filter().order_by('name'),
        'generic' : Generic.objects.filter().order_by('name'),
        'sub_generic' : SubGeneric.objects.filter().order_by('name'),
        'brand' : Brand.objects.filter().order_by('name'),
        'item_unit' : Unit.objects.filter().order_by('name'),
	}
    return render(request, 'inventory/in.html', context)

def inventory_list(request):
    return render(request, 'inventory/list.html')
