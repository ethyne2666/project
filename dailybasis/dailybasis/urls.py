"""
URL configuration for dailybasis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

admin.site.site_header = "Daily Basis Admin"
admin.site.site_title = "Daily Basis Admin Portal"
admin.site.index_title = "Welcome to Daily Basis Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dbApp.urls')),
    path('contact/', include('dbApp.urls')),
    path('aboutus/', include('dbApp.urls')),
    path('myProfile/', include('dbApp.urls')),
    path('header/', include('dbApp.urls')),
    path('cart/', include('dbApp.urls')),
    path('login/', include('dbApp.urls')),
    path('signup/', include('dbApp.urls')),
    path('checkout/', include('dbApp.urls')),
    path('services/', include('dbApp.urls')),
    path('logoutUser/', include('dbApp.urls')),

]
