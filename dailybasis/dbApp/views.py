from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from dbApp.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import UserData,Product ,ProductImage
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q # Import Q object for complex queries





def aboutus(request):
    return render(request,'dbApp/aboutus.html')

def myProfile(request):
    return render(request,'dbApp/myProfile.html')

# Signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # check if user exists
        if UserData.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")
        if UserData.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        # create user
        UserData.objects.create(
            username=username,
            email=email,
            phone=phone,
            password=password   # ⚠ storing plain password (ok for demo only)
        )
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "dbApp/signup.html")


# Login view
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = UserData.objects.get(username=username, password=password)
            # store session
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")  # redirect to home/dashboard
        except UserData.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "dbApp/login.html")


# Dashboard (only if logged in)
def dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "Please login first")
        return redirect("login")

    user = UserData.objects.get(id=user_id)
    return render(request, "dbApp/myProfile.html", {"user": user})


# Logout
def logout(request):
    request.session.flush()  # clears session
    messages.success(request, "Logged out successfully")
    return redirect("login")

def myProfile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserData.objects.get(id=user_id)
    return render(request, 'dbApp/myProfile.html', {'user': user})


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

def product_detail(request, product_id):
    # This is a placeholder. You would normally fetch a product from your database here.
    # For now, let's use some dummy data.
    try:
        product = {
            'id': product_id,
            'name': 'Sample Product',
            'description': 'This is a detailed description of the sample product.',
            'price': 499,
            'image_url': 'images/placeholder_product.jpg'
        }
    except Exception as e:
        # Handle the case where the product ID doesn't exist
        # In a real app, you would use get_object_or_404(Product, pk=product_id)
        return render(request, 'dbApp/error.html', {'message': 'Product not found'})

    context = {
        'product': product
    }
    return render(request, 'dbApp/product_detail.html', context)



def index(request):
    # Fetch all products from the database and pass them to the template
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'dbApp/index.html', context)

def details_page(request, product_id):
    product = get_object_or_404(Product.objects.prefetch_related('images'), pk=product_id)
    
    # Fetch related products from the same category
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'dbApp/details_page.html', context)

# All your other views (contact, login, signup, etc.) are fine as they are.
# I will not change them based on your request.
def cart_view(request):
    return render(request, 'dbApp/cart.html')


def search_results(request):
    query = request.GET.get('query')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'dbApp/search_results.html', context)