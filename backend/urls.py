from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView)
    
urlpatterns = [
    # path('', admin.site.urls),
    path('', include('account.urls')),
    path('', include('group.urls')),
    path('', include('products.urls')),
    
    # Open API 자체를 조회
    path('api/docs/', SpectacularAPIView.as_view(), name='schema'),

    # Open API Document UI로 조회: Swagger, Redoc
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]