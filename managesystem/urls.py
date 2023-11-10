from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('selectfilter/', views.selectfilter_view, name='selectfilter'),
    path('informationstaff/',views.informationstaff_view,name='informationstaff'),
    path('informationuser/',views.informationuser_view,name='informationuser'),
    path('formreport/',views.formreport_view,name='formreport'),
    path('formreportuser/',views.formreportuser_view,name='formreportuser'),
    path('report/<int:employee_id>/', views.report_view, name='report')

]