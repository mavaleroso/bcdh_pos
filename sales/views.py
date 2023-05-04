from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Clients, Items, ClientType)
import json 
from django.core import serializers
import datetime
from django.contrib.auth.hashers import make_password

from django.db.models import F

@csrf_exempt
def salestransaction(request):
    context = {
		'clients' : Clients.objects.filter().order_by('first_name'),
    'items' : Items.objects.filter().select_related()
	}
    return render(request, 'sales/transaction.html', context)

    
@csrf_exempt
def patientdetails(request):
    patient_id = request.POST.get('patient')
    qs_list = list(
         (Clients.objects
             .filter(id=patient_id)
             .select_related('client_type')
             .values('first_name','middle_name','last_name', 'client_type__name')
         )
    )
    return JsonResponse({'data': qs_list})


        





