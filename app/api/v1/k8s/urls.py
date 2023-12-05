from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.endpoints, name='endpoints'),
    path('nodes/', views.GetNodes, name='nodes'),
    path('pods/', views.GetPods, name='pods'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('my-api/', MyApiView.as_view(), name='my-api')
]
