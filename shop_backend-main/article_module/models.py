from django.db import models
from jdatetime import datetime as jdatetime_datetime
import jdatetime


# Create your models here.

class ArticleCategory(models.Model):
    title = models.CharField(verbose_name='نام دسته بندی مقاله', max_length=50)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


class Article(models.Model):
    title = models.CharField(verbose_name='عنوان مقاله', max_length=100)
    image = models.ImageField(verbose_name='تصویر مقاله', upload_to='images/articles', null=True, blank=True)
    short_description = models.CharField(verbose_name='توضیحات کوتاه مقاله', max_length=100)
    full_description = models.TextField(verbose_name='توضیحات تکمیلی مقاله', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    jalali_created_date = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    @staticmethod
    def convert_to_persian_digits(number: int | str) -> str:
        persian_digits = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        }
        return ''.join(persian_digits.get(d, d) for d in str(number))

    def _build_jalali_from_dt(self, dt):
        jdt = jdatetime.datetime.fromgregorian(datetime=dt)
        persian_day = jdt.day
        persian_year = jdt.year
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
            super(Article, self).save(update_fields=['jalali_created_date'])
