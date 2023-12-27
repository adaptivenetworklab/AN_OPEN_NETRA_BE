from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('nodes', views.GetNodes, name='nodes'),
    path('pods', views.GetPods, name='pods'),
    path('pods/create', views.CreatePod, name='createpod'),
    path('namespaces', views.GetNamespaces, name='namespaces'),
    path('namespaces/create', views.CreateNamespace, name='createnamespaces'),
    path('deployments', views.GetDeployments, name='deployments'),
    path('services', views.GetServices, name='services'),
]
