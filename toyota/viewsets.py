from rest_framework import viewsets, mixins, generics
from .models import Product, Category
from toyota.serializers import ProductSerializer, CategorySerialaizer, CategoryCustomSerializer


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerialaizer


class CategoryCustomViewSet(viewsets.ViewSetMixin, mixins.ListModelMixin, generics.GenericAPIView): #viewsets.GenericViewSet

    """custom viewset for show in url - 'category_products' only names of products in category with id
     from url address, (look at urls and custom serializer CategoryCustomSerializer )"""

    queryset = Product.objects.all()
    serializer_class = CategoryCustomSerializer

    def get_queryset(self):
        self.queryset = Product.objects.filter(category__id=self.kwargs['id'])
        return self.queryset


"""looking for a new methods to display filds list to custom options not thru serializer but thru viewsets"""






