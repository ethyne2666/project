


from django.contrib import admin
from django.urls import path
from dbApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index,name='index'),    
    path('cart/', views.cart_view,name='cart'),
    path('contact/', views.contact,name='contact'),
    path('aboutus/', views.aboutus,name='aboutus'),
    path('myProfile/', views.myProfile,name='myProfile'),
    path('login/', views.login,name='login'),
    path('signup/', views.signup,name='signup'),
    path('checkout/', views.checkout,name='checkout'),
    path('services/', views.checkout,name='services'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="logout"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]