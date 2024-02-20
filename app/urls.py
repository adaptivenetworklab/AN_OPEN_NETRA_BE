from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.reverse, name='reverse'),
    path('user-management/create-user', views.CreateUser, name='create-user'),
    path('user-management/update-user/<int:user_id>', views.UpdateUser, name='update-user'),
    path('user-management/delete-user/<int:user_id>', views.DeleteUser, name='delete-user'),
    path('auth/login', views.LoginPage, name='login'),
    path('auth/logout', views.LogoutPage, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user-info', views.get_user_info, name='user-info'),
    path('user-management', views.UserManagement, name='user-management'),
    path('monitoring', views.monitoring, name='monitoring'),
    path('introduction', views.introduction, name='introduction'),
    path('monitoring/test', views.some_view, name='monitoring-test'),
    path('pyshark/test', views.capture_packets, name='pyshark-test'),
]  