from django.contrib import admin
from django.urls import path
from dbApp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),    
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('myProfile/', views.myProfile, name='myProfile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('services/', views.services, name='services'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logoutUser, name="logout"),
    path("search_results/", views.search_results, name="search_results"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),

    # Corrected and simplified product detail page URL
    path('product/<int:product_id>/', views.details_page, name='details_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)