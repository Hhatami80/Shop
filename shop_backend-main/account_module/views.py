from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

import sms_manager
from .models import User, PhoneOTP, ExpiringToken, Address
from .serializers import UserSerializer, LoginSerializer, SendOTPSerializer, VerifyOTPSerializer, UserAdminSerializer, \
    ForgetPasswordSerializer, ResetPasswordSerializer, AddressSerializer
from django.utils.timezone import timedelta
from .utils import is_strong_password
from django.utils.crypto import get_random_string


# Create your views here.

class RegisterView(APIView):
    def post(self, request: Request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            username = user_serializer.validated_data.get('username')
            user_phone = user_serializer.validated_data.get('phone')
            user_pass = user_serializer.validated_data.get('password')
            strong, message = is_strong_password(user_pass)
            if not strong:
                return Response({'errors': message}, status.HTTP_422_UNPROCESSABLE_ENTITY)

            user: User = User.objects.filter(username=username).first()
            if user is not None:
                return Response({'errors': 'این نام کاربری قابل استفاده نیست.'}, status.HTTP_400_BAD_REQUEST)
            otp_obj, _ = PhoneOTP.objects.update_or_create(phone=user_phone, username=username, password=user_pass)
            if sms_manager.send_otp(user_phone, otp_obj.code):
                return Response({'detail': 'کد تایید ارسال شد.'}, status.HTTP_200_OK)

        return Response({'errors': user_serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyOTPView(APIView):
    def post(self, request: Request):
        verify_serializer = VerifyOTPSerializer(data=request.data)
        if verify_serializer.is_valid():
            # user_phone = verify_serializer.validated_data.get('phone')
            user_code = verify_serializer.validated_data.get('code')

            # phone=user_phone,
            otp_object = PhoneOTP.objects.filter(code=user_code).last()

            if not otp_object:
                return Response({'errors': 'کد وارد شده صحیح نیست'}, status.HTTP_400_BAD_REQUEST)

            if otp_object.is_expired():
                return Response({'errors': 'کد وارد شده منقضی شده است'}, status.HTTP_400_BAD_REQUEST)

            # Todo: Create User
            user = User.objects.create(
                username=otp_object.username,
                phone=otp_object.phone,
            )
            ExpiringToken.objects.create(user=user)
            user.set_password(otp_object.password)
            user.save()

            otp_object.delete()

            return Response({'detail': 'اکانت با موفقیت ایجاد شد', 'data': {
                'username': user.username,
                'password': user.password,
                'is_active': user.is_active,
            }}, status.HTTP_200_OK)
        return Response({'errors': verify_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request: Request):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            user_name = login_serializer.validated_data.get('username')
            user_pass = login_serializer.validated_data.get('password')
            user: User = User.objects.filter(username__iexact=user_name).first()
            if user is not None:
                is_password_correct = user.check_password(user_pass)
                if is_password_correct:
                    if user.is_active:

                        token = ExpiringToken.objects.filter(user=user).first()
                        if token and token.is_expired():
                            token.delete()

                        token, _ = ExpiringToken.objects.get_or_create(user=user)
                        return Response({'token': token.key, 'expires': token.created + timedelta(days=1),
                                         'user': UserAdminSerializer(user).data},
                                        status.HTTP_200_OK)
                    else:
                        return Response({'errors': 'اکانت کاربر فعال نیست'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

                else:
                    return Response({'errors': {'password': 'اطلاعات وارد شده اشتباه میباشد'}},
                                    status.HTTP_422_UNPROCESSABLE_ENTITY)

            else:
                return Response({'errors': {'username': 'اطلاعات وارد شده اشتباه میباشد'}},
                                status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response({'errors': login_serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            user = request.user
            token = ExpiringToken.objects.get(user=user)
            token.delete()
            return Response({'detail': 'کاربر با موفقیت خارج شد'}, status=status.HTTP_200_OK)
        except (AttributeError, ExpiringToken.DoesNotExist):
            return Response({'detail': 'خطا در خروج ار حساب کاربری'}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    def post(self, request: Request):
        forget_pass = ForgetPasswordSerializer(data=request.data)
        if forget_pass.is_valid():
            phone = forget_pass.validated_data.get('phone')


class ResetPasswordView(APIView):
    def put(self, request: Request):
        user = request.user
        reset_pass = ResetPasswordSerializer(user, data=request.data)
        if reset_pass.is_valid():
            new_pass = reset_pass.validated_data.get('password')
            strong, message = is_strong_password(new_pass)
            if not strong:
                return Response({'errors': message}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({'detail': 'پسوورد جدید ایجاد شد'},
                                status.HTTP_200_OK)
        return Response({'errors': reset_pass.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        address = Address.objects.get(request.user)
        address_serializer = AddressSerializer(address, many=True)
        return Response({'data': address_serializer.data}, status.HTTP_200_OK)

    def post(self, request: Request):
        address_serializer = AddressSerializer(data=request.data)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response({'data': address_serializer.data}, status.HTTP_200_OK)
        return Response({'errors': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, address_id: int):
        address = Address.objects.get(pk=address_id)
        address_serializer = AddressSerializer(address, data=request.data)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response({'data': address_serializer.data}, status.HTTP_200_OK)
        return Response({'data': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, address_id: int):
        address = Address.objects.get(pk=address_id)
        address.delete()
        return Response({'data': 'Address deleted successfully'})
