from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def login(request):
    return render(request, 'login.html')

@csrf_exempt
def dashboard(request):
    return render(request, 'dashboard.html')

