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


class ProductIMG(models.Model):
    img = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)


class Basket(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    def sum_of_basket(self):
        #
        #learn in_bulk()
        sum_list = []
        for prod in self.productinbasket_set.all(): #productinbasket_set - it is a reverce link to ProductInBasket class
            sum_list.append(prod.price_per_weight)
        return sum(sum_list)

    def __str__(self):
        return f'basket of {self.user.username}'


class ProductInBasket(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=3)

    @property
    def price_per_weight(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.basket}'


class Order(models.Model):
    date_of_order = models.DateField(auto_now=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    sum = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def sum_of_order(self):
        result = sum(self.productinorder_set.all().values_list('price', flat=True))
        self.sum = result
        self.save()
        return result


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=3)
    price = models.DecimalField(max_digits=8, decimal_places=2)

