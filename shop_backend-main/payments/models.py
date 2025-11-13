import uuid

from django.db import models
from Shop import settings


# Create your models here.
class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELED = "canceled", "Canceled"

    class Type(models.TextChoices):
        Order = "پرداخت سفارش", "Order"
        WalletCharge = "شارژ کیف پول", "WalletCharge"
        WalletWithdraw = "برداشت از کیف پول", "WalletWithdraw"
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=20, decimal_places=0)
    reference_id = models.CharField(max_length=100, null=True, blank=True, default="INTERNAL_PAYMENT")
    internal_tracking_id = models.CharField(max_length=100, unique=True)
    gateway = models.CharField(max_length=50, default="manual")  # or "zarinpal", "paypal", etc.
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.WalletCharge)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"

    @staticmethod
    def generate_tracking_id():
        return uuid.uuid4().hex[:12].upper()

    def save(self, *args, **kwargs):
        if not self.internal_tracking_id:
            self.internal_tracking_id = self.generate_tracking_id()
        super().save(*args, **kwargs)