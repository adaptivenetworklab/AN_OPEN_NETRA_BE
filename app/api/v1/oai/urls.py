from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('create-cu', views.CreateCU, name='cu'),
    path('create-du', views.CreateDU, name='du'),
    path('create-ue', views.CreateUE, name='ue'),
    path('update-values', views.update_values, name='values'),
]