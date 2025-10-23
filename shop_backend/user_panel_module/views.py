from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UpdatePasswordSerializer, UpdateProfileSerializer, AddressSerializer, BankInfoSerializer
from account_module.models import User
from account_module.utils import is_strong_password
from account_module.models import BankInformation, Address


# Create your views here.

class PasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        user = request.user
        password_serializer = UpdatePasswordSerializer(user, data=request.data)
        if password_serializer.is_valid():
            new_pass = password_serializer.validated_data.get('password')
            strong, message = is_strong_password(new_pass)
            if not strong:
                return Response({'errors': message}, status.HTTP_422_UNPROCESSABLE_ENTITY)

            user_current_pass = password_serializer.validated_data.get('current_password')
            if user.check_password(user_current_pass):
                password_serializer.save()
                return Response({'detail': 'Password updated successfully'},
                                status.HTTP_200_OK)
            else:
                return Response({'errors': 'current password is incorrect'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({'errors': password_serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        profile_serializer = UpdateProfileSerializer(user, context={'request': request})
        return Response({'data': profile_serializer.data}, status.HTTP_200_OK)

    def put(self, request: Request):
        user = request.user
        profile_serializer = UpdateProfileSerializer(user, data=request.data, context={'request': request})
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({'detail': 'Profile updated successfully'},
                            status.HTTP_200_OK)
        return Response({'errors': profile_serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class BankInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        try:
            bank_info = BankInformation.objects.get(user=user)
        except BankInformation.DoesNotExist:
            # No bank info found for this user
            return Response({'bankAccounts': None}, status=status.HTTP_200_OK)

        serializer = BankInfoSerializer(bank_info)
        return Response({'bankAccounts': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request: Request):
        request.data['user'] = request.user.id
        bank_info_serializer = BankInfoSerializer(data=request.data)
        if bank_info_serializer.is_valid():
            bank_info_serializer.save()
            return Response({'bankAccounts': bank_info_serializer.data}, status.HTTP_200_OK)
        return Response({'errors': bank_info_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request):
        user = request.user
        bank_info_serializer = BankInfoSerializer(user, data=request.data)
        if bank_info_serializer.is_valid():
            bank_info_serializer.save()
            return Response({'detail': 'Bank information updated'}, status.HTTP_200_OK)
        return Response({'errors': bank_info_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        bank_info = BankInformation.objects.get(user=request.user)
        bank_info.delete()
        return Response({'data': 'Bank information deleted successfully'})


class AddressInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        address = Address.objects.get(user=user)
        address_serializer = BankInfoSerializer(address, many=True)
        return Response({'address': address_serializer.data}, status.HTTP_200_OK)

    def post(self, request: Request):
        request.data['user'] = request.user.id
        address_serializer = BankInfoSerializer(data=request.data)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response({'address': address_serializer.data}, status.HTTP_200_OK)
        return Response({'errors': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request):
        user = request.user
        address_serializer = BankInfoSerializer(user, data=request.data)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response({'detail': 'Address information updated'}, status.HTTP_200_OK)
        return Response({'errors': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        user = request.user
        address = Address(user=user)
        address.delete()
        return Response({'data': 'Address information deleted successfully'})


# class ProfileImageUpdateView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request: Request):
#         user = request.user
#         user_image = UpdateProfileImageSerializer(user, many=True, context={'request': request})
#         return Response({'data': user_image.data}, status.HTTP_200_OK)
#
#     def put(self, request: Request):
#         user = request.user
#         image_serializer = UpdateProfileImageSerializer(user, data=request.data, context={'request': request})
#         if image_serializer.is_valid():
#             image_serializer.save()
#             return Response({'detail': 'Profile Image updated successfully'},
#                             status.HTTP_200_OK)
#         return Response({'errors': image_serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
