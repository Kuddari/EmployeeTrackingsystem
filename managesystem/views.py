from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request,"login.html")

def selectfilter_view(request):
    return render(request,"selectfilter.html")

def informationstaff_view(request):
    return render(request,"informationstaff.html")

def informationuser_view(request):
    return render(request,"informationuser.html")

def formreport_view(request):
    return render(request,"formreport.html")

def report_view(request):
    return render(request,"report.html")