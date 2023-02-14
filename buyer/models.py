
from django.db import models
from seller.models import Product

# Create your models here.
class Buyer(models.Model):
    First_name  = models.CharField(max_length= 50)
    Last_name  = models.CharField(max_length= 70)
    Email = models.EmailField(unique= True) 
    Password  = models.CharField(max_length=15)
    Address = models.TextField(max_length=500)
    Phone = models.CharField(max_length=15)
    Pic = models.FileField(upload_to='Buyer_profile',default='sad.jpg')

    def __str__(self):
        return self.First_name

class Cart(models.Model):
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.buyer)
    
