from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.timezone import now, timedelta
from django.conf import settings

import random


# Create your models here.

class ExpiringToken(Token):
    created_date = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration = self.created_date + timedelta(days=30)
        return now() > expiration

    def time_left(self):
        expiration = self.created_date + timedelta(days=30)
        return expiration - now()


class User(AbstractUser):
    ROLE_CHOICE_ADMIN = 'admin'
    ROLE_CHOICE_USER = 'user'

    ROLE_CHOICE = (
        (ROLE_CHOICE_ADMIN, 'admin'),
        (ROLE_CHOICE_USER, 'user'),
    )

    phone = models.CharField(unique=True, null=False,max_length=13, blank=False, default=0, error_messages={
        'unique': 'این شماره تلفن در سیستم وجود دارد.'
    })
    is_active = models.BooleanField(default=True)
    fullname = models.CharField(null=True, blank=True,max_length=255, verbose_name='نام کاربری')
    image = models.ImageField(verbose_name='پروفایل کاربر', upload_to='images/profiles', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default=ROLE_CHOICE_USER)
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.phone} ({self.get_role_display()})'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    full_address = models.CharField(max_length=500)
    plate = models.IntegerField()
    unit = models.IntegerField()
    postal_code = models.IntegerField()

    def __str__(self):
        return f'{self.user} -> {self.city}'


class BankInformation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_infos')
    cardNumber = models.CharField(max_length=16, verbose_name='شماره کارت')
    iban = models.CharField(max_length=36, verbose_name='شماره شبا')
    accountNumber = models.CharField(max_length=12, verbose_name='شماره حساب')

    def __str__(self):
        return f'{self.user}'


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    def is_expired(self):
        expiration = self.created_at + timedelta(minutes=2)
        return now() > expiration

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.phone} - {self.code}'
