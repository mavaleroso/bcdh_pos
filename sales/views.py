from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (Clients)
import json 
from django.core import serializers
import datetime
from django.contrib.auth.hashers import make_password


def salestransaction(request):
    context = {
		'clients' : Clients.objects.filter().order_by('first_name')
	}
    return render(request, 'sales/transaction.html', context)


        





