from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *


def login_view(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(username=request.user)
            if employee.position == 'Dean':
                return redirect('selectfilter')
            else:
                return redirect('informationuser')
        except Employee.DoesNotExist:
            messages.error(request, "ไม่มีชื่อผู้ใช้ในระบบ")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                employee = Employee.objects.get(username=user)
                if employee.position == 'Dean':
                    return redirect('selectfilter')
                else:
                    return redirect('informationuser')
            except Employee.DoesNotExist:
                return redirect('login')
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render(request, 'login.html')

@login_required
def selectfilter_view(request):
    try:
        employee = Employee.objects.get(username=request.user)
        if employee.position != 'Dean':
            return redirect('informationuser')
    except Employee.DoesNotExist:
        return redirect('informationuser')

    return render(request, "selectfilter.html")

@login_required
def informationstaff_view(request):
    # Get the position query parameter from the URL
    selected_position = request.GET.get('position', None)

    if selected_position is None:
        # If no query parameter is provided, show all employees
        employees = Employee.objects.all()
    else:
        # Filter employees based on the query parameter
        employees = Employee.objects.filter(position=selected_position)

    context = {
        "employees": employees,
    }

    return render(request, "informationstaff.html", context)

@login_required
def informationuser_view(request):
    
    return render(request, "informationuser.html")

@login_required
def formreport_view(request):

    return render(request, "formreport.html")

@login_required
def report_view(request):
    
    return render(request, "report.html")
    