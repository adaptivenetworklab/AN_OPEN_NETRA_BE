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

    path('single-cu-restart', views.RestartSingleCU, name='single-cu-restart'),
    path('single-du-restart', views.RestartSingleDU, name='single-du-restart'),
    path('single-ue-restart', views.RestartSingleUE, name='single-ue-restart'),
    path('multignb-cu-restart', views.RestartMultignbCU, name='multignb-cu-restart'),
    path('multignb-du1-restart', views.RestartMultignbDU1, name='multignb-du1-restart'),
    path('multignb-du2-restart', views.RestartMultignbDU2, name='multignb-du2-restart'),
    path('multignb-ue-restart', views.RestartMultignbUE, name='multignb-ue-restart'),
    path('multiue-cu-restart', views.RestartMultiueCU, name='multiue-cu-restart'),
    path('multiue-du-restart', views.RestartMultiueDU, name='multiue-du-restart'),
    path('multiue-ue1-restart', views.RestartMultiueUE1, name='multiue-ue1-restart'),
    path('multiue-ue2-restart', views.RestartMultiueUE2, name='multiue-ue2-restart'),
]
