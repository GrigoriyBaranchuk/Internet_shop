from django.contrib import admin
from toyota.models import Category, Product, ProductIMG, ProductInBasket, Basket, Order

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductIMG)
admin.site.register(ProductInBasket)
admin.site.register(Basket)
admin.site.register(Order)

