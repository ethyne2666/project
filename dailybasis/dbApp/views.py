from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from dbApp.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import UserData,Product ,ProductImage, Address
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q # Import Q object for complex queries
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt






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
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()

    selected_category = request.GET.get('category')
    sort_option = request.GET.get('sort')

    # Filter by category
    if selected_category:
        products = products.filter(category=selected_category)

    # Sort by price
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'sort': sort_option
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





# releated to cart



def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            product = get_object_or_404(Product, id=product_id)
            
            cart = request.session.get('cart', {})
            
            # Update quantity if product is already in cart
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] += quantity
            else:
                cart[str(product_id)] = {
                    'name': product.name,
                    'price': str(product.price), # Convert Decimal to string for JSON serialization
                    'image': product.image.url if product.image else '',
                    'quantity': quantity
                }
            
            request.session['cart'] = cart
            
            # Return a JSON response for success
            return JsonResponse({'success': True, 'message': f'"{product.name}" added to cart!', 'item_count': len(cart)})
        
        except (json.JSONDecodeError, Product.DoesNotExist) as e:
            return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = 0

    for product_id, item_data in cart.items():
        item_price = float(item_data['price'])
        total_item_price = item_price * item_data['quantity']
        subtotal += total_item_price
        
        cart_items.append({
            'product_id': product_id,
            'name': item_data['name'],
            'image': item_data['image'],
            'price': item_price,
            'quantity': item_data['quantity'],
            'total_price': total_item_price
        })

    delivery_fee = 4.99
    total = subtotal + delivery_fee

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total
    }
    return render(request, 'dbApp/cart.html', context)


def saved_addresses(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')
    user = UserData.objects.get(id=user_id)
    addresses = Address.objects.filter(user=user)
    return render(request, 'dbApp/saved_addresses.html', {'addresses': addresses})

def add_address(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')
    if request.method == "POST":
        address_line = request.POST.get("address_line")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        country = request.POST.get("country", "India")  # default value

        Address.objects.create(
            user=UserData.objects.get(id=user_id),
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            country=country
        )
        messages.success(request, "Address added successfully!")
        return redirect("saved_addresses")

    return render(request, "dbApp/add_address.html")

def delete_address(request, address_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')
    try:
        address = Address.objects.get(id=address_id, user_id=user_id)
        address.delete()
        messages.success(request, "Address deleted successfully!")
    except Address.DoesNotExist:
        messages.error(request, "Address not found.")
    return redirect("saved_addresses")