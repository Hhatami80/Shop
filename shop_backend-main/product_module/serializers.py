from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product, ProductCategory, Brand, ProductProperty, ProductComment, ProductGallery, ProductTag, Cart, \
    CartItem, ProductRating, OrderItem, Order, CategoryBanner, Wallet, WalletTransaction, Payment
from mixins.dedup_image_serializer import DedupImageMixin
from django.utils import timezone
import json
from django.http import QueryDict
import jdatetime
from account_module.serializers import UserAdminSerializer, UserSerializer


class ProductMiniSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'image']


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    image_field_name = 'image'
    categories = ProductMiniSerializer(read_only=True, many=True)

    class Meta:
        model = ProductCategory
        exclude = ['slug']


class ProductPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperty
        fields = ['key', 'value']


class ProductGallerySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductGallery
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    parser_classes = [MultiPartParser, FormParser]
    image = serializers.ImageField(use_url=True)
    images = ProductGallerySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        write_only=True
    )
    properties = ProductPropertySerializer(many=True)
    # is_favorited = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = CategorySerializer(read_only=True)
        self.fields['category_id'] = serializers.PrimaryKeyRelatedField(
            queryset=ProductCategory.objects.all(),
            write_only=True
        )

    def to_internal_value(self, data):
        if isinstance(data, QueryDict):
            mutable = data.dict()
        else:
            try:
                mutable = dict(data)
            except Exception:
                mutable = data.copy() if hasattr(data, 'copy') else data

        if 'properties' in mutable and isinstance(mutable['properties'], str):
            try:
                mutable['properties'] = json.loads(mutable['properties'])
            except json.JSONDecodeError:
                raise serializers.ValidationError(
                    {'properties': 'Invalid JSON format. Use [{"key":"k","value":"v"}, ...]'})
        return super().to_internal_value(mutable)

    # def get_is_favorited(self, obj):
    #     user = self.context.get('request').user
    #     if user.is_authenticated:
    #         return obj.favorited_by.filter(user=user).exists()
    #     return False

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return 0

    def get_comment_count(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def create(self, validated_data):
        request = self.context.get('request')
        properties_data = validated_data.pop('properties', [])
        category = validated_data.pop('category_id')
        product = Product.objects.create(category=category, **validated_data)
        uploaded_images = request.FILES.getlist('uploaded_images')
        if uploaded_images:
            for image in uploaded_images:
                ProductGallery.objects.create(product=product, image=image)

        for prop in properties_data:
            if not isinstance(prop, dict):
                continue
            if 'key' in prop and 'value' in prop:
                ProductProperty.objects.create(product=product, key=prop['key'], value=prop['value'])
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        properties_data = validated_data.pop('properties', None)
        category = validated_data.pop('category_id', None)
        
        uploaded_images = request.FILES.getlist('uploaded_images')
        if uploaded_images:
            for image in uploaded_images:
                ProductGallery.objects.create(product=instance, image=image)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if category:
            instance.category = category

        instance.save()

        if properties_data is not None:
            instance.properties.all().delete()

            for prop in properties_data:
                if not isinstance(prop, dict):
                    continue
                if 'key' in prop and 'value' in prop:
                    ProductProperty.objects.create(
                        product=instance,
                        key=prop['key'],
                        value=prop['value']
                    )

        return instance


class BrandSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Brand
        fields = ['id', 'title', 'image', 'price', 'sub_title']


class ProductCommentSerializer(serializers.ModelSerializer):

    product = ProductMiniSerializer()
    user = UserSerializer()
    
    class Meta:
        model = ProductComment
        fields = '__all__'
        read_only_fields = ['user', 'product', 'parent']

    def create(self, validated_data):
        now = timezone.now()
        jdt = jdatetime.datetime.fromgregorian(datetime=now)

        def convert_to_persian_digits(number):
            persian_digits = {
                '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
                '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
            }
            return ''.join(persian_digits.get(d, d) for d in str(number))

        persian_day = convert_to_persian_digits(jdt.day)
        persian_year = convert_to_persian_digits(jdt.year)
        persian_months = [
            "", "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]
        persian_month = persian_months[jdt.month]

        validated_data['jalali_created_date'] = f"{persian_day} {persian_month} {persian_year}"
        return super().create(validated_data)


class ProductDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description']



class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['product', 'rating']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("امتیازدهی باید بین 1 تا 5 باشد.")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['items', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'price']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'gateway',
            'is_successful',
            'payment_method',
            'authority',
            'ref_id',
            'created_at'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    created_at_jalali = serializers.SerializerMethodField()
    user = UserAdminSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'total_price',
            'items',
            'payment',
            'created_at',
            'created_at_jalali'
        ]
        read_only_fields = ["user", "total_price", "created_at"]

    def get_created_at_jalali(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.created_at).strftime("%d %B %Y")

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item_data in items_data:
            product = item_data.pop('product')
            quantity = item_data['quantity']
            price = item_data['price']
            total += quantity * price
            OrderItem.objects.create(order=order, product=product, **item_data)
        order.total_price = total
        order.save()
        return order


class CategoryBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBanner
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = ['id', 'type', 'method', 'amount', 'description', 'date']

    def get_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")


class WalletSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ['balance', 'transactions']

