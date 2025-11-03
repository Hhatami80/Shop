from rest_framework import serializers
from .models import Article
from django.utils import timezone
import jdatetime


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

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
