


from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view,name='cart'),
]