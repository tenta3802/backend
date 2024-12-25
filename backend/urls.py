from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('', admin.site.urls),
    path('', include('account.urls')),
    path('', include('group.urls'))
]
