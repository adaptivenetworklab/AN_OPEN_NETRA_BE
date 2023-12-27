from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('auth/signup', views.SignupPage, name='signup'),
    path('auth/login', views.LoginPage, name='login'),
    path('auth/logout', views.LogoutPage, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/projects', views.project_list),
    path('deploy', views.deploy, name='deploy'),
    path('images', views.images, name='images'),
    path('services', views.services, name='services'),
    path('users', views.user_list),
    path('users/<str:username>', views.UserDetail.as_view()),

]  