from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('selectfilter/', views.selectfilter_view, name='selectfilter'),
    path('',views.informations_view,name='informations'),

]