from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def login(request):
    return render(request, 'login.html')

@csrf_exempt
def dashboard(request):
    return render(request, 'index.html')
