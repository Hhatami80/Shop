from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UpdatePasswordSerializer, UpdateProfileSerializer, BankInfoSerializer
from account_module.models import User
from account_module.utils import is_strong_password
from account_module.models import BankInformation, Address, City, Province
from account_module.serializers import CitySerializer, ProvinceSerializer, AddressSerializer
import requests
from django.conf import settings


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
            return Response({'bankAccounts': None}, status=status.HTTP_200_OK)

        serializer = BankInfoSerializer(bank_info)
        return Response({'bankAccounts': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request: Request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = BankInfoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'bankAccounts': serializer.data}, status=status.HTTP_200_OK)
        else:
            print("Serializer errors:", serializer.errors)
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request):
        user = request.user
        try:
            bank_info = BankInformation.objects.get(user=user)
        except BankInformation.DoesNotExist:
            return Response({'detail': 'Bank info not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankInfoSerializer(bank_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Bank information updated'}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BankInfoDeleteView(APIView):
    def delete(self, request: Request, bank_id: int):
        try:
            bank_info = BankInformation.objects.get(id=bank_id, user=request.user)
        except BankInformation.DoesNotExist:
            return Response({'detail': 'Bank information not found'}, status=status.HTTP_404_NOT_FOUND)

        bank_info.delete()
        return Response({'data': 'Bank information deleted successfully'}, status=status.HTTP_200_OK)


class ProvinceListView(APIView):
    def get(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityListView(APIView):
    def get(self, request):
        province_id = request.query_params.get('province')

        if province_id:
            cities = City.objects.filter(province_id=province_id)
        else:
            cities = City.objects.all()

        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        address = Address.objects.filter(user=request.user).first()

        if address:
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        else:

            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Address.objects.get(pk=pk, user=user)
        except Address.DoesNotExist:
            return None

    def get(self, request, pk):
        address = self.get_object(pk, request.user)
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk, request.user)
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk, request.user)
        if not address:
            return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({'detail': 'Address deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# class PaymentRequestView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         amount = request.data.get('amount')
#         payment = Payment.objects.create(user=request.user, amount=amount)
#
#         data = {
#             "merchant_id": settings.ZARINPAL_MERCHANT_ID,
#             "amount": amount,
#             "callback_url": settings.ZARINPAL_CALLBACK_URL,
#             "description": "خرید از فروشگاه تستی",
#         }
#
#         response = requests.post(settings.ZARINPAL_REQUEST_URL, json=data)
#         result = response.json()
#
#         if result['data']['code'] == 100:
#             authority = result['data']['authority']
#             payment.authority = authority
#             payment.save()
#             link = f"{settings.ZARINPAL_STARTPAY_URL}{authority}"
#             return Response({"link": link})
#         else:
#             return Response({"error": result['errors']}, status=400)
#
#
# class PaymentVerifyView(APIView):
#     def get(self, request):
#         authority = request.GET.get('Authority')
#         status_param = request.GET.get('Status')
#
#         try:
#             payment = Payment.objects.get(authority=authority)
#         except Payment.DoesNotExist:
#             return Response({"detail": "Invalid authority"}, status=404)
#
#         if status_param != 'OK':
#             return Response({"detail": "Payment canceled by user"}, status=400)
#
#         data = {
#             "merchant_id": settings.ZARINPAL_MERCHANT_ID,
#             "amount": payment.amount,
#             "authority": authority,
#         }
#         response = requests.post(settings.ZARINPAL_VERIFY_URL, json=data)
#         result = response.json()
#
#         if result['data']['code'] == 100:
#             payment.is_paid = True
#             payment.ref_id = result['data']['ref_id']
#             payment.save()
#             return Response({"detail": "Payment successful", "ref_id": payment.ref_id})
#         else:
#             return Response({"detail": "Payment failed", "result": result}, status=400)

# class AddressInformationView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request: Request):
#         user = request.user
#         try:
#             address = Address.objects.get(user=user)
#         except Address.DoesNotExist:
#             # No bank info found for this user
#             return Response({'address': None}, status=status.HTTP_200_OK)
#
#         address_serializer = BankInfoSerializer(address, many=True)
#         return Response({'address': address_serializer.data}, status.HTTP_200_OK)
#
#     def post(self, request: Request):
#         request.data['user'] = request.user.id
#         address_serializer = BankInfoSerializer(data=request.data)
#         if address_serializer.is_valid():
#             address_serializer.save()
#             return Response({'address': address_serializer.data}, status.HTTP_200_OK)
#         return Response({'errors': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request: Request):
#         user = request.user
#         address_serializer = BankInfoSerializer(user, data=request.data)
#         if address_serializer.is_valid():
#             address_serializer.save()
#             return Response({'detail': 'Address information updated'}, status.HTTP_200_OK)
#         return Response({'errors': address_serializer.errors}, status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request: Request):
#         user = request.user
#         address = Address(user=user)
#         address.delete()
#         return Response({'data': 'Address information deleted successfully'})


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
