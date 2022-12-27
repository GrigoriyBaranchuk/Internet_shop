"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from toyota.views import *
from rest_framework import routers
from toyota.viewsets import ProductViewSet, CategoryViewSet, CategoryCustomViewSet, ProductsInBasketViewSet, CreateOrderViewSet


router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register(prefix=r'category/(?P<id>\d+)/products', viewset=CategoryCustomViewSet)
router.register('basket', ProductsInBasketViewSet)
router.register('buy', CreateOrderViewSet)



api = [path('api/', include(router.urls)),
       # path('api/category/<int:id>/products', CategoryCustomViewSet.as_view({"get": "list"}),
       #      name='category_products'),
       ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='index'),
    path('category/<int:category_pk>', category_details, name='category_details'),
    path('product_details/<int:product_pk>', product_details, name='product_details'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_request, name='register'),
    path('add_to_basket/<int:product_pk>', add_product_to_basket, name='add_product_to_basket'),
    path('basket/<int:user_pk>', user_basket, name='user_basket'),
    path('delete_product_from_basket/<int:product_in_basket_pk>', delete_product_from_basket,
         name='delete_product_from_basket'),
    path('change_quantity/<str:action>/<int:product_in_basket_pk>', action_with_product_weight,
         name='change_quantity'),
    path('buy/<int:basket>', buy, name='buy'),
] + api
