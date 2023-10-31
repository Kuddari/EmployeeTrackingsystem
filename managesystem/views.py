from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.conf import settings


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
    if request.method == 'POST':
    # Get the selected position
        selected_position = request.GET.get('position')
        
        # Retrieve the relevant Indicator objects based on the selected position
        indicators = Indicator.objects.all()  # You may need to filter this based on your specific criteria
    
        for indicator in indicators:
            # Build the field names based on the indicator's ID
            units_for_deans = request.POST.get(f'unitsfordeans_{indicator.id}')
            units_for_lecturers = request.POST.get(f'unitsforlecturers_{indicator.id}')
            units_for_employees = request.POST.get(f'unitsforemployees_{indicator.id}')
            
            # Update the indicator based on the selected position
            if selected_position == 'Dean':
                indicator.unitsfordeans = units_for_deans
            elif selected_position == 'Lecturer':
                indicator.unitsforlecturers = units_for_lecturers
            elif selected_position == 'Researcher':
                indicator.unitsforemployees = units_for_employees

            indicator.save()

        return HttpResponseRedirect(reverse('informationstaff') + f'?position={selected_position}')


    selected_position = request.GET.get('position')

    if selected_position is None:
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(position=selected_position)
    work_units = WorkUnit.objects.filter(employee__in=employees)

    context = {
        'employees': employees,
        'work_units': work_units,
        'selected_position': selected_position,
    }

    return render(request, 'formreport.html', context)




def formreportuser_view(request):
    return render(request,'formreportuser.html')

@login_required
def report_view(request):
    
    return render(request, "report.html")
    