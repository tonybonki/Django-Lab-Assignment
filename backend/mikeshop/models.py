from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass

class Product(models.Model):
    id = models.AutoField(primary_key=True),
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null = False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    product_image = models.FileField(upload_to='products')

    def __str__(self):
        return self.name

class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_id}'s Basket" 

class BasketItem(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.basket_id} item" 

def price(self):
	return self.product_id.price * self.quantity

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)