from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (UserDetails, RoleDetails, AuthUser )


def get_user_details(request):
    return UserDetails.objects.filter(user_id=request.user.id).first()


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return redirect("login")


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            auth_login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['fullname'] = user.first_name + user.last_name
            return redirect("dashboard")
        
        elif user is None:
            messages.error(request, 'Invalid Username or Password/blocked.')
        
        else:
            messages.error(request, 'Your account is blocked')

    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    user_details = get_user_details(request)
    
    allowed_roles = ["Admin", "Management"]
    
    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'user_role' : role.role_name,
        'role_permission': role.role_name,
    }

    return render(request, 'dashboard.html',context)


@csrf_exempt
def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect("login")
