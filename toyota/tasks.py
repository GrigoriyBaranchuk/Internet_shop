from celery import shared_task
from toyota.models import ProductInBasket, Basket, Product
from django.contrib.auth.models import User


@shared_task
def add_some_product_to_admin_basket():
    product_in_admin_basket = ProductInBasket(basket_id=2,
                                              product_id=2,
                                              quantity=2)
    product_in_admin_basket.save()

