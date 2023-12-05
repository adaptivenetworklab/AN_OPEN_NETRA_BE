from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('nodes/', views.GetNodes, name='nodes'),
    path('pods/', views.GetPods, name='pods'),
    path('namespaces/', views.GetNamespaces, name='namespaces'),
    path('deployments/', views.GetDeployments, name='deployments'),
    path('services/', views.GetServices, name='services'),
]
