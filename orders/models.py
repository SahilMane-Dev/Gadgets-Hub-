from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
from products.models import Product

class Order(models.Model):

    STATUS_CHOCIES =[
        ("PENDING" , "Pending"),
        ("SHIPPED" , "Shipped"),
        ("DELIVERED" , "Delivered"),
        ("CANCELLED" , "Cancelled"),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(max_length= 20 , choices= STATUS_CHOCIES , default= "PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE , related_name="items")
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)


    def __str__(self):
        return  f"{self.product} x {self.quantity}"