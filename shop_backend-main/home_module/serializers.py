from rest_framework import serializers
from product_module.models import Product
from product_module.serializers import ProductPropertySerializer


class ProductMainPageSerializer(serializers.ModelSerializer):
    properties = ProductPropertySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'discount', 'price', 'discounted_price', 'is_done', 'properties', 'short_description', 'description']


class BestSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'image']