from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('single-cu-config', views.ConfigSingleCU, name='single-cu'),
    path('single-du-config', views.ConfigSingleDU, name='single-du'),
    path('single-ue-config', views.ConfigSingleUE, name='single-ue'),
    path('multignb-cu-config', views.ConfigMultignbCU, name='multignb-cu'),
    path('multignb-du1-config', views.ConfigMultignbDU1, name='multignb-du1'),
    path('multignb-du2-config', views.ConfigMultignbDU2, name='multignb-du2'),
    path('multignb-ue-config', views.ConfigMultignbUE, name='multignb-ue'),
    path('multiue-cu-config', views.ConfigMultiueCU, name='multiue-cu'),
    path('multiue-du-config', views.ConfigMultiueDU, name='multiue-du'),
    path('multiue-ue1-config', views.ConfigMultiueUE1, name='multiue-ue1'),
    path('multiue-ue2-config', views.ConfigMultiueUE2, name='multiue-ue2'),
    path('create-all-5g', views.CreateAll5G, name='all5g'),
]