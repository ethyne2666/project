from django.contrib import admin
from django.urls import path,include
from dbApp import views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),    
    path('index/', views.index, name='index'),    
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('myProfile/', views.myProfile, name='myProfile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('services/', views.services, name='services'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logoutUser, name="logout"),
    path("search_results/", views.search_results, name="search_results"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('saved_addresses/', views.saved_addresses, name='saved_addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path("gemini-chat/", views.gemini_chat, name="gemini_chat"),
    path("check-username/", views.check_username, name="check_username"),
    path("payment/", views.payment_page, name="payment"),
    path("process-payment/", views.process_payment, name="process_payment"),


    # Corrected and simplified product detail page URL
    path('product/<int:product_id>/', views.details_page, name='details_page'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('subscriptions/add/', views.purchase_schedule, name='purchase_schedule'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)