from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request, 'dbApp/index.html')

def product_list(request):
    # placeholder: later replace with Product.objects.all()
    return render(request, 'dbApp/product_list.html', {'products': []})

def product_detail(request, pk):
    # placeholder
    return render(request, 'dbApp/product_detail.html', {'product_id': pk})

def cart_view(request):
    return render(request, 'dbApp/cart.html')

