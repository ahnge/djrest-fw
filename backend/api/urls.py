
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home),
    # products
    path('products/', views.ProductListApiView.as_view()),
    path('products/create/', views.ProductListCreateApiView.as_view()),
    path('products/<int:pk>/', views.ProductDetailApiView.as_view()),
    path('products/test/', views.product_alt_view)
]
