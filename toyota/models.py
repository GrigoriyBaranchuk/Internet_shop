from django.db import models
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    stock = models.DecimalField(max_digits=6, decimal_places=3, default=0.000)

    def __str__(self):
        return f'{self.name}'

    def price_per_weight(self):
        price_per_weight = self.price * self.stock
        return price_per_weight


class ProductIMG(models.Model):
    img = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)


class Basket(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'basket of {self.user.username}'


class ProductInBasket(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return f'{self.basket}'
