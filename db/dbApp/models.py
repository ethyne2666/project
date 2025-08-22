from django.db import models

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