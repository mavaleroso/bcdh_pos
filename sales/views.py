from django.shortcuts import render

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


def salestransaction(request):
    # context = {
	# 	'users' : AuthUser.objects.filter().exclude(id=1).order_by('first_name').select_related('userdetails')
	# }
    return render(request, 'sales/transaction.html')


        





