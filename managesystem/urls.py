from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('selectfilter/', views.selectfilter_view, name='selectfilter'),
    path('informationstaff/',views.informationstaff_view,name='informationstaff'),
    path('',views.informationuser_view,name='informationuser'),
    path('formreport/',views.formreport_view,name='formreport'),
    path('report',views.report_view,name='report'),
]