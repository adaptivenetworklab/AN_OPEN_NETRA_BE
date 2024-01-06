from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('api/v1/tokens/', include('app.api.v1.token.urls')),
    path('api/v1/k8s/', include('app.api.v1.k8s.urls')),
    path('api/v1/oai/', include('app.api.v1.oai.urls')),
]
