from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect,Http404,HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import itertools
from django.core.paginator import Paginator
from datetime import datetime



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
    employee = Employee.objects.get(username=request.user)
    results = Result.objects.all()
    
    grouped_works = {key: list(group) for key, group in itertools.groupby(results, key=lambda x: x.work.name.name)}
    
    if request.method == 'POST' and request.FILES:
        for result in results:
            file_input_name = f'fileInput-{result.id}'
            if file_input_name in request.FILES:
                file = request.FILES[file_input_name]

                # Validate file extension
                if not file.name.endswith('.zip'):
                    return HttpResponseBadRequest("Invalid file format. Please upload a ZIP file.")
                # Try to get an existing Result record
                existing_result = Result.objects.filter(employee=employee, work=result.work).first()

                if existing_result:
                    # Update the existing record
                    existing_result.file = file
                    existing_result.save()
                else:
                    # Create a new record
                    new_result = Result.objects.create(employee=employee, work=result.work, file=file)
                    new_result.save()
               
        return HttpResponseRedirect(reverse('informationuser'))

    context = {
        'grouped_works': grouped_works,
        'results': results,
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
    else :
        return HttpResponseRedirect(reverse('selectfilter'))

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
        'employee': employee
    }
    return render(request, "report.html", context)


def delete_data_view(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete all records in the Setunit table
        Setunit.objects.all().delete()

        # Delete all records in the Result table
        Result.objects.all().delete()

        # Redirect to a success page or any other page you desire
        return redirect('informationstaff')

    # Render a template with a button to trigger the deletion
    return render(request, 'delete_data.html')

def conclusion_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    results = Result.objects.filter(employee=employee)
    grouped_works = {key: list(group) for key, group in itertools.groupby(results, key=lambda x: x.work.name.name)}
    total_sum = (results.aggregate(Sum('total'))['total__sum'] or 0)
    score_sum = (results.aggregate(Sum('result_score'))['result_score__sum'] or 0)
    result_sum = float(score_sum / 10)
    
    if request.method == 'POST':
        for group_name, group_works in grouped_works.items():
            for work in group_works:
                employee_score = float(request.POST.get(f'employee_score_{work.id}',0))
                dean_score = float(request.POST.get(f'dean_score_{work.id}',0))
                userresult, created = Result.objects.get_or_create(employee=employee, work=work.work)
                # Update or create minunit and maxunit values
                userresult.employee_score = employee_score
                userresult.dean_score = dean_score
                userresult.result_score = work.total * dean_score
                userresult.save()
        if work.employee_score != float(0):
                for result in results:
                    save_obj = Save(
                        employee_id = result.employee.username,
                        employee_firstname = result.employee.username.first_name,
                        employee_lastname = result.employee.username.last_name,
                        work=result.work.name.name,
                        description=result.work.name.description,
                        total=result.total,
                        employee_score = result.employee_score,
                        dean_score = work.total * dean_score,
                        result_score = result.result_score,
                        file=result.file, 
                    )
                    save_obj.save()        
        return HttpResponseRedirect(reverse('selectfilter'))

    context = {
        'grouped_works': grouped_works,
        'employee': employee,
        'total_sum': total_sum,
        'score_sum': score_sum,
        'result_sum': result_sum
    }

    return render(request,"conclusion.html", context)

def download_file_view(request, result_id):
    # Try to get the result from the Result model
    result = Result.objects.filter(id=result_id).first()

    # Try to get the Save from the Save model
    report_file = Save.objects.filter(id=result_id).first()

    # Check if either Result or Save is found
    if result:
        file_path = result.file.path
    elif report_file:
        file_path = report_file.file.path
    else:
        raise Http404("File not found")

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={result.file.name if result else report_file.file.name}'

    return response

def work_history_view(request):
    workdata_history = Save.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    employee_query = request.GET.get('employee')
    work_history_employee = Save.objects.filter(employee_id = request.user)
    employee_choices = Employee.objects.values_list('username__first_name', 'username__last_name').distinct().order_by('username__first_name')


    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%d/%m/%Y') if start_date else None
    end_date = datetime.strptime(end_date, '%d/%m/%Y') if end_date else None


    if start_date:
        workdata_history = workdata_history.filter(date__gte=start_date)
        work_history_employee =  work_history_employee.filter(date__gte=start_date)
    
    if end_date:
        workdata_history = workdata_history.filter(date__lte=end_date)
        work_history_employee =  work_history_employee.filter(date__lte=end_date)
    
    if employee_query:
        workdata_history = workdata_history.filter(employee_firstname=employee_query)


    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Number of items to display per page (you can customize this)
    items_per_page = request.GET.get('items_per_page', 10)  # Default to 10 items per page

    # Create a Paginator instance
    paginator = Paginator(workdata_history, items_per_page)

    # Get the current page's data
    page_data = paginator.get_page(page_number)

    # Pass the data to the template
    context = {
        'workdata_history': page_data,
        'work_history_employee':work_history_employee,
        'employee_choices' : employee_choices,
        'start_date' : start_date,
        'end_date' : end_date,
        'items_per_page': items_per_page,
    }


    return render(request,"work_history.html", context)