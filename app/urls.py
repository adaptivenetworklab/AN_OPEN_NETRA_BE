from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.reverse, name='reverse'),
    path('user-account-management/create-user', views.CreateUser, name='create-user'),
    path('auth/login', views.LoginPage, name='login'),
    path('auth/logout', views.LogoutPage, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user-management', views.UserManagement, name='user-management'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('introduction', views.introduction, name='introduction'),
]  