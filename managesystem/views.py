from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import itertools


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
    selected_position = request.GET.get('position', None)
    if selected_position is None:
        # If no query parameter is provided, show all employees
        employees = Employee.objects.all()
    else:
        # Filter employees based on the query parameter
        employees = Employee.objects.filter(position=selected_position)


    context = {
        "employees": employees,
        'position' : selected_position
    }

    return render(request, "informationstaff.html", context)

def informationuser_view(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']  # Accessing the uploaded file from the form

        # Save the file to the database
        file_model = File.objects.create(file=file) 
        file_model.save()

        messages.success(request, 'File saved successfully!')
        return HttpResponseRedirect(reverse('informationuser'))

    result = Result.objects.all()
    grouped_works = {key: list(group) for key, group in itertools.groupby(result, key=lambda x: x.work.name.name)}

    context = {
        'grouped_works': grouped_works
    }

    return render(request, "informationuser.html", context)

@login_required
def formreport_view(request):
    selected_position = request.GET.get('position')
    unit = Setunit.objects.filter(position=selected_position)
    works = None  # Define works variable

    if selected_position == 'Dean':
        if unit.exists() and unit.first().position == 'Dean':
            works = Setunit.objects.filter(position=selected_position)
            grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name.name)}
        else:
            works = Work.objects.all()
            grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name)}
    elif selected_position == 'Lecturer':
        if unit.exists() and unit.first().position == 'Lecturer':
            works = Setunit.objects.filter(position=selected_position)
            grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name.name)}
        else:
            works = Work.objects.all()
            grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name)}
    elif selected_position == 'Researcher':
        if unit.exists() and unit.first().position == 'Researcher':
            works = Setunit.objects.filter(position=selected_position)
            grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name.name)}
        else:
            works = Work.objects.all()
            grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name)}
            
    if request.method == 'POST':
        # Handle form submission and update or create Setunit records
        for group_name, group_works in grouped_works.items():
            for work in group_works:
                minunit = request.POST.get(f'minunit_{work.id}')
                maxunit = request.POST.get(f'maxunit_{work.id}')
                if unit:
                    setunit, created = Setunit.objects.get_or_create(name=work.name, position=selected_position)
                else:
                    setunit, created = Setunit.objects.get_or_create(name=work, position=selected_position)

                # Update or create minunit and maxunit values
                setunit.minunit = minunit
                setunit.maxunit = maxunit
                setunit.save()

        return HttpResponseRedirect(reverse('informationstaff') + f'?position={selected_position}')

    context = {
        'grouped_works': grouped_works,
        'selected_position': selected_position,
    }

    return render(request, 'formreport.html', context)


def formreportuser_view(request):
    employee = Employee.objects.get(username=request.user)
    results = Result.objects.filter(employee=employee)
    works = []
    total = 0
    result = 0
    
    if results:
        works = Result.objects.filter(employee=employee)
        grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.work.name.name)}
    else:
        works = Setunit.objects.filter(position=employee.position)
        grouped_works = {key: list(group) for key, group in itertools.groupby(works, key=lambda x: x.name.name)}

    if request.method == 'POST':
        # Handle form submission and update or create Setunit records
        for group_name, group_works in grouped_works.items():
            for work in group_works:
                term1 = request.POST.get(f'term1_{work.id}')
                term2 = request.POST.get(f'term2_{work.id}')
                term1 = int(term1) if term1.isdigit() else 0
                term2 = int(term2) if term2.isdigit() else 0
                total = term1 + term2
                
                if results:
                    userresult, created = Result.objects.get_or_create(employee=employee, work=work.work)
                else:
                    userresult, created = Result.objects.get_or_create(employee=employee, work=work)


                # Update or create minunit and maxunit values
                userresult.term1 = term1
                userresult.term2 = term2
                userresult.total = total
                userresult.total = total

                userresult.save()

        return HttpResponseRedirect(reverse('informationuser'))
    
    context = {
        'grouped_works': grouped_works,
        'employee': employee
    }
    return render(request, 'formreportuser.html', context)


@login_required
def report_view(request, employee_id):
    # Get the employee based on the provided employee_id
    employee = get_object_or_404(Employee, id=employee_id)
    results = Result.objects.filter(employee=employee)

    # Assuming you want to group by work name
    grouped_works = {key: list(group) for key, group in itertools.groupby(results, key=lambda x: x.work.name.name)}

    context = {
        'grouped_works': grouped_works,
        'results': results,
    }
    return render(request, "report.html", context)
