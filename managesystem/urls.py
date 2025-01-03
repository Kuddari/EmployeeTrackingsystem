from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.Log_out, name='logout'),
    path('selectfilter/', views.selectfilter_view, name='selectfilter'),
    path('informationstaff/',views.informationstaff_view,name='informationstaff'),
    path('informationuser/',views.informationuser_view,name='informationuser'),
    path('formreport/',views.formreport_view,name='formreport'),
    path('formreportuser/',views.formreportuser_view,name='formreportuser'),
    path('report/<int:employee_id>/', views.report_view, name='report'),
    path('delete_data/', views.delete_data_view, name='delete_data'),
    path('conclusion/<int:employee_id>/', views.conclusion, name='conclusion'),
    path('conclusion_view/<int:employee_id>/', views.conclusion_view, name='conclusion_view'),
    path('final_conclusion/<int:employee_id>/', views.Final, name='final_conclusion'),
    path('download_file/<int:result_id>/', views.download_file_view, name='download_file'),
    path('work_history/', views.work_history_view, name='work_history'),
    path('total/', views.Total, name='total'),
    path('register/', views.register_view, name='register'),

]