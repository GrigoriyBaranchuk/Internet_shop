from rest_framework import serializers, viewsets
from toyota.models import Product, Category, ProductInBasket, ProductInOrder, Order, Basket


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
                  'products',
                  )


class CategoryCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',
                  )


class ProductsBasketSerializer(serializers.ModelSerializer):
    product = CategoryCustomSerializer(read_only=True)
    class Meta:
        model = ProductInBasket
        fields = ('basket',
                  'product',
                  'quantity',
                  'price_per_weight',
                  )


class ProductsInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = ('id',
                  'product',
                  'quantity',
                  'price',
                  )


class OrderSerializer(serializers.ModelSerializer):
    products = ProductsInOrderSerializer(many=True, source='productinorder_set', read_only=True)

    class Meta:
        model = Order
        fields = ('id',
                  'date_of_order',
                  'products')

    def create(self, validated_data):
        user = self.context['request'].user
        basket = Basket.objects.filter(user=user).first()
        products = ProductInBasket.objects.filter(basket_id=basket.id)
        if products:
            order = Order.objects.create(basket=basket)
            for prod in products:
                ProductInOrder.objects.create(order=order,
                                              product=prod.product,
                                              quantity=prod.quantity,
                                              price=prod.price_per_weight,
                                              )
            order.sum_of_order()
            products.delete()
            return order
        return {}
