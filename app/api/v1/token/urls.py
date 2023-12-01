from django.urls import path, include
from . import views
from .views import MyTokenObtainPairView, MyApiView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-api/', MyApiView.as_view(), name='my-api')
]