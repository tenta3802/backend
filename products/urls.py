from django.urls import path
import products.views

urlpatterns = [
    path('product/', products.views.ProductCreateList.as_view(), name='productList'),
    path('product/register/', products.views.ProductCreateList.as_view(), name='productList'),
]
