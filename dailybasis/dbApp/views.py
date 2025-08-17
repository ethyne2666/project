from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from dbApp.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login as auth_login

def index(request):
    if request.user.is_anonymous:
        messages.warning(request, "You are not logged in. Please log in to access all features.")
        return redirect('/login')
    return render(request, 'dbApp/index.html')


def cart_view(request):
    return render(request, 'dbApp/cart.html')


def aboutus(request):
    return render(request,'dbApp/aboutus.html')

def myProfile(request):
    return render(request,'dbApp/myProfile.html')

def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)  # log the user in
            return redirect('dbApp/index.html')   # use the URL name of your home page
        else:
            # stay on the same login page with error message
            return render(request, 'dbApp/login.html', {'error': 'Invalid username or password'})

    return render(request, 'dbApp/login.html')

def signup(request):
    return render(request, 'dbApp/signup.html')

def checkout(request):
    return render(request,'dbApp/checkout.html')


def services(request):
    return render(request,'dbApp/services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,phone=phone,desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Contact form has been submitted.")
        
        return render(request, 'dbApp/contact.html', {'success': True})
    return render(request,'dbApp/contact.html')

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('dbApp/index')



