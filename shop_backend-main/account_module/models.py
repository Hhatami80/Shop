import os, random
from pathlib import Path

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


def get_image():
    images_dir = os.path.join(settings.MEDIA_ROOT, 'images', 'profiles', 'defaults')
    image = os.listdir(images_dir)[0]
    return f'images/profiles/defaults/{image}'


class User(AbstractUser):
    ROLE_CHOICE_ADMIN = 'admin'
    ROLE_CHOICE_USER = 'user'

    ROLE_CHOICE = (
        (ROLE_CHOICE_ADMIN, 'admin'),
        (ROLE_CHOICE_USER, 'user'),
    )

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    phone = models.CharField(max_length=100, unique=True, null=False, blank=False, default=0, error_messages={
        'unique': 'این شماره تلفن در سیستم وجود دارد.'
    })
    is_active = models.BooleanField(default=True)
    image = models.ImageField(verbose_name='پروفایل کاربر', upload_to='images/profiles',
                              null=True, blank=True, default=get_image)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default=ROLE_CHOICE_USER)
    birthdate = models.DateField(blank=True, null=True)
    
    
    
    def __str__(self):
        return f'{self.username} - {self.phone} ({self.get_role_display()})'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f'{self.name} ({self.province})'


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    full_address = models.CharField(max_length=500)
    plate = models.IntegerField()
    # unit = models.IntegerField()
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    neighborhood = models.CharField(null=True, max_length=255)
    street = models.CharField(null=True ,max_length=255)

    def __str__(self):
        return f'{self.user} -> {self.city}'


class BankInformation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_infos')
    cardNumber = models.CharField(max_length=100, verbose_name='شماره کارت')
    iban = models.CharField(max_length=100, verbose_name='شماره شبا')
    accountNumber = models.CharField(max_length=100, verbose_name='شماره حساب')

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
