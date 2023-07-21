from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import (UserDetails, RoleDetails, AuthUser, StocksItems, OutItems, StockLocation, Clients )
from django.db.models import Sum


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

    #Overall
    stock = StocksItems.objects.aggregate(total_pcs_quantity=Sum('pcs_quantity'))
    out = OutItems.objects.aggregate(total_quantity=Sum('quantity'))
    total_stock_pcs_quantity = stock['total_pcs_quantity'] if stock['total_pcs_quantity'] is not None else 0
    total_out_quantity = out['total_quantity'] if out['total_quantity'] is not None else 0
    total_overall = total_stock_pcs_quantity - total_out_quantity
    #EndOverall

    #Main
    main = OutItems.objects.filter(location_id = 1).aggregate(total_quantity=Sum('quantity'))
    location = StockLocation.objects.filter(location_id = 1).aggregate(total_quantity=Sum('quantity'))
    total_main_quantity = main['total_quantity'] if main['total_quantity'] is not None else 0
    total_location_quantity = location['total_quantity'] if location['total_quantity'] is not None else 0
    total_main = total_location_quantity - total_main_quantity
    # EndMain

    #Emergency
    emergency = OutItems.objects.filter(location_id = 2).aggregate(total_quantity=Sum('quantity'))
    emg_location = StockLocation.objects.filter(location_id = 2).aggregate(total_quantity=Sum('quantity'))
    emg_quantity = emergency['total_quantity'] if emergency['total_quantity'] is not None else 0
    emg_location_quantity = emg_location['total_quantity'] if emg_location['total_quantity'] is not None else 0
    total_emergency = emg_location_quantity - emg_quantity
    #EndEmergency

    #Others
    others = OutItems.objects.filter(location_id = 3).aggregate(total_quantity=Sum('quantity'))
    oth_location = StockLocation.objects.filter(location_id = 3).aggregate(total_quantity=Sum('quantity'))
    oth_quantity = others['total_quantity'] if others['total_quantity'] is not None else 0
    oth_location_quantity = oth_location['total_quantity'] if oth_location['total_quantity'] is not None else 0
    total_others = oth_location_quantity - oth_quantity
    #EndEmergency

    #Client type count
    walk_in = Clients.objects.filter(client_type_id=1).count()
    out_patient = Clients.objects.filter(client_type_id=2).count()
    in_patient = Clients.objects.filter(client_type_id=3).count()
    #end   

    user_id = request.session.get('user_id', 0)

    # UserDetails.objects.filter(user_id=user_id).select_related().first()

    



    role = RoleDetails.objects.filter(id=user_details.role_id).first()
    context = {
        'user_role' : role.role_name,
        'role_permission': role.role_name,
        'overall': total_overall,
        'main': total_main,
        'emergency': total_emergency,
        'others': total_others,
        'walk_in':walk_in,
        'out_patient':out_patient,
        'in_patient':in_patient,
        # 'role_name': role_name

    }
    return render(request, 'dashboard.html',context)





@csrf_exempt
def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect("login")
