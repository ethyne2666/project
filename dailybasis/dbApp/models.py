from django.db import models
from django.utils import timezone


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=122) 
    email =  models.EmailField(max_length=122)
    phone =  models.CharField(max_length=15,blank=True,null=True) 
    desc = models.TextField(max_length=500) 
    date = models.DateField(blank=True,null=True)

    def __str__(self):
            return self.name
     
class UserData(models.Model):
    username = models.CharField(max_length=122, unique=True)
    email = models.EmailField(max_length=122, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255)  # will store hashed password

    def __str__(self):
        return self.username
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='General') # e.g., Fruits, Dairy, Bakery
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/') # Images will be stored in media/products/
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"Image for {self.product.name}"



# New Address model
class Address(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.address_line}, {self.city}"
    


# class purchases(models.Model):
#     user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='orders')
#     order_date = models.DateTimeField(default=timezone.now)
#     status = models.CharField(max_length=50, default='Pending')  # Pending, Shipped, Delivered, Cancelled
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def _str_(self):
#         return f"Orders #{self.id} by {self.user.username}"


# class purchasesItems(models.Model):
#     order = models.ForeignKey(purchases, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.PositiveIntegerField(default=1)
#     price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

#     def _str_(self):
#         return f"{self.quantity} x {self.product.name} for Order #{self.purchases.id}"