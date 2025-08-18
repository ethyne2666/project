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