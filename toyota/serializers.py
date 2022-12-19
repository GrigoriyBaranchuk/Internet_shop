from rest_framework import serializers, viewsets
from toyota.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'price',
                  'category',
                  'stock',
                  )


class CategorySerialaizer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
                                 # source='product_set')

    class Meta:
        model = Category
        fields = ('id',
                  'name',
                  'products'
                  )

