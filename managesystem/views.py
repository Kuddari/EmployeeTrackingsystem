from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request,"login.html")

def selectfilter_view(request):
    return render(request,"selectfilter.html")

def informations_view(request):
    return render(request,"informations.html")