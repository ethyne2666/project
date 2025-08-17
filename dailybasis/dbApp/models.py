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
     
