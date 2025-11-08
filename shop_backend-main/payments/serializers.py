from rest_framework import serializers
from .models import Transaction
from account_module.models import User


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'user')