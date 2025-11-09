from rest_framework import serializers
from account_module.models import User, Address, BankInformation
import jdatetime


class UpdatePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True, write_only=True, error_messages={
        'required': 'پسوورد فعلی خالی است',
        'blank': 'پسوورد فعلی نمیتواند خالی باشد',
    })

    confirm_password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'تکرار پسوورد خالی است',
        'blank': 'تکرار پسوورد نمیتواند خالی باشد',
    })

    class Meta:
        model = User
        fields = ['current_password', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'error_messages': {
                    'required': 'پسوورد خالی است',
                    'blank': 'پسوورد نمیتواند خالی باشد'
                }
            },
        }

    # def validate(self, data):
    #     if len(data) < 6:
    #         raise serializers.ValidationError("پسوورد کوتاه است")
    #     return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInformation
        fields = '__all__'

import jdatetime
from rest_framework import serializers

class JalaliDateField(serializers.DateField):
    def to_internal_value(self, value):
        if isinstance(value, str) and "/" in value:
            try:
                jy, jm, jd = map(int, value.split("/"))
                return jdatetime.date(jy, jm, jd).togregorian()
            except Exception:
                raise serializers.ValidationError(
                    "Invalid Jalali date format. Expected jYYYY/jMM/jDD."
                )
        return super().to_internal_value(value)


class UpdateProfileSerializer(serializers.ModelSerializer):
    birthdate = JalaliDateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'image', 'birthdate', 'first_name', 'last_name']

# class UpdateProfileImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['image']
