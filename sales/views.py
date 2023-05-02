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
    # clients = Clients.objects.filter(id=patient_id).select_related()
    # qs_json = serializers.serialize('json', clients, fields=['first_name', 'middle_name', 'client_type__name'])

    # clients = (Clients.objects
    # .filter(id=patient_id )
    # .select_related('client_type')
    # #use F to evaluate supplier_type__name and add to new field
    # .annotate(client_type_name = F('client_type__name'))
    # )
    # qs_json = serializers.serialize(
    #     'json', 
    #     clients, 
    #     #use our new field for serialization
    #     fields=['first_name', 'middle_name', 'client_type__name']
    # )


    clients = Clients.objects.filter(client_type_id=patient_id)
    qs_json = serializers.serialize('json', clients, fields=['first_name', 'middle_name','last_name',  'client_type__name'])

    print("watmeme")
    print(qs_json) 
    return JsonResponse({'data': qs_json})








# def patientdetails(request):
    
#     patient_id = request.POST.get('patient')
#     # patient_details = Clients.objects.filter(id=patient_id).select_related()
    
#     # qs_json = serializers.serialize('json', patient_details)


#     context = {
# 		'company' : Clients.objects.filter(id=patient_id).select_related("clientType__name")
    
# 	}

#     # qs_json = serializers.serialize('json', context)

#     # tabledata = Clients.objects.filter(id=patient_id).annotate(creator_name=F('creator__name')).values()
        

#     # return JsonResponse(qs_json)

    
#     # patient_id = request.POST.get('patient')
#     # patient_details = Clients.objects.filter(id=patient_id).select_related()
    
#     qs_json = serializers.serialize('json', context)
#     return JsonResponse({'data': qs_json})

        





