from django.db import models
from django.utils.text import slugify
from jalali_date import date2jalali
# from slugify import slugify
from django.utils.text import slugify
from account_module.models import User
from jdatetime import datetime as jdatetime_datetime
import jdatetime
from django.conf import settings


# import hashlib, os


# Create your models here.

class ProductCategory(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    parent = models.ForeignKey('ProductCategory', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children')
    image = models.ImageField(verbose_name='عکس دسته بندی', upload_to='images/categories', null=True, blank=True)
    link = models.CharField(verbose_name='لینک مقصد',max_length=200, null=True, blank=True)
    slug = models.SlugField(default='', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.title}'
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Brand(models.Model):
    title = models.CharField(verbose_name='برند محصول', max_length=100, null=True, blank=True)
    image = models.ImageField(verbose_name='عکس برند', upload_to='images/brands')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class ProductTag(models.Model):
    tag = models.CharField(verbose_name='عنوان تگ', max_length=50)

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'

    def __str__(self):
        return self.tag


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان محصول')
    image = models.ImageField(verbose_name='عکس محصول', upload_to='images/products', null=True, blank=True)
    slug = models.SlugField(default='', null=True, blank=True)
    short_description = models.CharField(verbose_name='توضیحات کوتاه', max_length=300,null=True, blank=True)
    description_title = models.CharField(verbose_name='عنوان توضیحات',max_length=200, null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات تکمیلی', null=True, blank=True)
    price = models.CharField(verbose_name='قیمت محصولات',max_length=100)
    discount = models.CharField(verbose_name='تخفیف', null=True, blank=True, max_length=20)
    discounted_price = models.CharField(verbose_name='قیمت تخفیف خورده', null=True, blank=True, max_length=20)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, verbose_name='برند محصول', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,max_length=255, verbose_name='دسته بندی محصول', default=1,
                                 related_name='categories')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی')
    # product_tag = models.ManyToManyField(ProductTag, verbose_name='تگ محصول')
    is_done = models.BooleanField(default=False, verbose_name='تمام شده / نشده')
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت محصول', editable=False, auto_now_add=True)
    jalali_created_date = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)

        # Calculate discounted price
        if self.discount:
            try:
                discount_amount = (int(self.discount) / 100) * float(self.price)
                self.discounted_price = int(float(self.price) - discount_amount)
                self.final_price = self.discounted_price
            except (ValueError, TypeError):
                self.discounted_price = None
        else:
            self.discounted_price = None
            self.final_price = self.price

        if not self.jalali_created_date and self.created_date:
            jalali_date = jdatetime_datetime.fromgregorian(datetime=self.created_date)
            self.jalali_created_date = f"{jalali_date.day} {jalali_date.strftime('%B')} {jalali_date.year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=30,
        choices=[('pending', 'Pending'), ('paid', 'Paid'), ('completed', 'Completed'), ('canceled', 'Canceled')],
        default='pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total(self):
        total = sum(item.quantity * item.price for item in self.items.all())
        self.total_price = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2 , max_length=200)


class ProductRating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)  # 1 to 5

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.product} -> ({self.rating})'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f'Cart for {self.user.name}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def total_price(self):
        return int(self.product.price) * self.quantity


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='favorites'
#     )
#     product = models.ForeignKey(
#         'Product',
#         on_delete=models.CASCADE,
#         related_name='favorited_by'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'product')
#
#     def __str__(self):
#         return f'{self.user} -> {self.product}'


class ProductProperty(models.Model):
    product = models.ForeignKey('Product', related_name='properties', on_delete=models.CASCADE, default=1)
    key = models.CharField(max_length=100, verbose_name='ویژگی')
    value = models.CharField(max_length=200, verbose_name='مقدار')

    def __str__(self):
        return f'{self.key}: {self.value}'

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصول'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('ProductComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    jalali_created_date = models.CharField(max_length=20, blank=True, null=True)
    text = models.TextField(verbose_name='متن نظر')
    is_approved = models.BooleanField(default=False, verbose_name='تایید شده / نشده')

    class Meta:
        verbose_name = 'کامنت محصول'
        verbose_name_plural = 'کامنت های محصول'

    def __str__(self):
        return f'{self.product} / {self.parent}'

    @staticmethod
    def convert_to_persian_digits(number: int | str) -> str:
        persian_digits = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        }
        return ''.join(persian_digits.get(d, d) for d in str(number))

    def _build_jalali_from_dt(self, dt):
        jdt = jdatetime.datetime.fromgregorian(datetime=dt)
        persian_day = self.convert_to_persian_digits(jdt.day)
        persian_year = self.convert_to_persian_digits(jdt.year)
        persian_months = [
            "", "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]
        persian_month = persian_months[jdt.month]
        return f"{persian_day} {persian_month} {persian_year}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.jalali_created_date:
            dt = self.created_date
            self.jalali_created_date = self._build_jalali_from_dt(dt)
            super(ProductComment, self).save(update_fields=['jalali_created_date'])


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, verbose_name='گالری محصول', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='تصویر', upload_to='images/product-gallery')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'تصاویر گالری'


class CategoryBanner(models.Model):

    title = models.CharField(verbose_name='عنوان بنر', max_length=100, default='')
    image = models.ImageField(verbose_name='بنر دسته بندی', upload_to='images/category_banner')

    def __str__(self):
        return f'{self.title} --> {self.title}'

    class Meta:
        verbose_name = 'بنر دسته بندی'
        verbose_name_plural = 'بنر های دسته بندی'