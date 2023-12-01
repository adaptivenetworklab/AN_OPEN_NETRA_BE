from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('getnodes/', views.GetNodes, name='getnodes'),
    # path('createpod/', views.CreatePod, name='createpod'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('my-api/', MyApiView.as_view(), name='my-api')
]