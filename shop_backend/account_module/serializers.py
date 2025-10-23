from rest_framework import serializers
from .models import User, Address


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role']


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'تکرار پسوورد خالی است',
        'blank': 'تکرار پسوورد نمیتواند خالی باشد',
    })

    class Meta:
        model = User
        fields = ['username', 'phone', 'password', 'confirm_password']
        extra_kwargs = {
            'username': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'نام کاربری خالی است',
                    'blank': 'نام کاربری نمی تواند خالی باشد',
                }
            },
            'phone': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'تلفن همراه خالی است',
                    'blank': 'تلفن همراه نمی تواند خالی باشد',
                }
            },
            'password': {
                'required': True,
                'error_messages': {
                    'required': 'پسوورد خالی است',
                    'blank': 'پسوورد نمی تواند خالی باشد',
                }
            },
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, error_messages={
        'required': 'نام کاربری خالی است',
        'blank': 'نام کاربری نمی تواند خالی باشد',
    })
    password = serializers.CharField(required=True, write_only=True, error_messages={
        'required': 'پسوورد خالی است',
        'blank': 'پسوورد نمی تواند خالی باشد',
    })


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class VerifyOTPSerializer(serializers.Serializer):
    # phone = serializers.CharField()
    code = serializers.CharField()


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']


class ResetPasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'تکرار پسوورد خالی است',
        'blank': 'تکرار پسوورد نمیتواند خالی باشد',
    })

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'error_messages': {
                    'required': 'پسوورد خالی است',
                    'blank': 'پسوورد نمیتواند خالی باشد'
                }
            },
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'