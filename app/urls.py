from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('user-account-management/create-user', views.CreateUser, name='create-user'),
    path('auth/login', views.LoginPage, name='login'),
    path('auth/logout', views.LogoutPage, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user-account-management', views.UserAccountManagement, name='uam'),
    path('user-plan-config', views.UserPlanConfig, name='upc'),
    path('ran-metric-graph', views.RanMetricGraph, name='rmg'),
]  