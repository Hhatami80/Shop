import json
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.db import transaction

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes

from account_module.models import User
from payments.models import Transaction
from .models import Product, ProductGallery, ProductComment, Cart, CartItem, ProductRating, OrderItem, Order, \
    CategoryBanner, ProductCategory, Payment, Wallet, WalletTransaction, WalletPayment
from .serializers import ProductSerializer, ProductGallerySerializer, ProductCommentSerializer, \
    ProductDescriptionSerializer, ProductPropertySerializer, CartItemSerializer, CartSerializer, \
    ProductRatingSerializer, OrderSerializer, CategoryBannerSerializer, CategorySerializer, WalletSerializer, \
    TransactionSerializer
from .services import create_order
from .filters import OrderFilter
from .pagination import DefaultPagination


# Create your views here.

class ProductDetailView(APIView):
    def get(self, request: Request, product_id):
        product = Product.objects.prefetch_related('images').filter(is_active=True).get(pk=product_id)
        comment = ProductComment.objects.filter(product=product, is_approved=True)
        product_serializer = ProductSerializer(product, context={'request': request})
        comment_serializer = ProductCommentSerializer(comment, many=True)
        product_gallery = ProductGallery.objects.filter(product_id=product_id)
        gallery_serializer = ProductGallerySerializer(product_gallery, many=True, context={'request': request})
        return Response({'product': product_serializer.data, 'gallery': gallery_serializer.data,
                         'comment': comment_serializer.data}, status.HTTP_200_OK)


class ApprovedCommentsView(APIView):
    def get(self, request: Request, product_id):
        comments = ProductComment.objects.filter(product_id=product_id, is_approved=True)
        comment_serializer = ProductCommentSerializer(comments, many=True)
        return Response({'comment': comment_serializer.data}, status.HTTP_200_OK)


class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, product_id):
        comments = ProductComment.objects.filter(product_id=product_id, is_approved=True)
        comment_serializer = ProductCommentSerializer(comments, many=True)
        return Response({'comments': comment_serializer.data}, status.HTTP_200_OK)

    def post(self, request: Request, product_id):
        product = get_object_or_404(Product, id=product_id)
        parent_id = request.data.get('parent')
        parent = None

        if parent_id:
            parent = get_object_or_404(ProductComment, id=parent_id)

        comment_serializer = ProductCommentSerializer(data=request.data)

        if comment_serializer.is_valid():
            # Save instance
            comment = comment_serializer.save(
                user=request.user,
                product=product,
                parent=parent,
            )
            new_serializer = ProductCommentSerializer(comment)

            return Response({'data': new_serializer.data}, status.HTTP_200_OK)

        return Response({'errors': comment_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class ProductDescriptionView(APIView):
    def get(self, request: Request, product_id):
        product = Product.objects.filter(is_active=True).get(id=product_id)
        des_serializer = ProductDescriptionSerializer(product)
        return Response(des_serializer.data, status.HTTP_200_OK)


class ProductPropertyView(APIView):
    def get(self, request: Request, product_id):
        product = Product.objects.get(id=product_id)
        product_property = product.properties.filter(product=product)
        property_serializer = ProductPropertySerializer(product_property, many=True)
        return Response({'specs': property_serializer.data}, status.HTTP_200_OK)


# class ToggleFavoriteView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request: Request, pk):
#         product = Product.objects.filter(pk=pk).first()
#         if not product:
#             return Response({'errors': 'محصول پیدا نشد'}, status.HTTP_404_NOT_FOUND)
#
#         favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
#         if not created:
#             favorite.delete()
#             return Response({'data': 'از محصولات مورد علاقه حذف شد'}, status.HTTP_200_OK)
#
#         return Response({'data': 'به محصولات مورد علاقه اضافه شد'}, status.HTTP_200_OK)
#
#
# class FavoriteListView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProductSerializer
#
#     def get_queryset(self):
#         return Product.objects.filter(favorite_by__user=self.request.user)


class SetProductRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = ProductRatingSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            rating = serializer.validated_data['rating']

            ProductRating.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating}
            )
            return Response({'message': 'امتیاز با موفقیت ثبت شد.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request: Request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart, context={'request': request}).data, status.HTTP_200_OK)

    def post(self, request: Request):
        cart = self.get_cart(request.user)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def patch(self, request: Request, cartitem_id: int):
        cart = self.get_cart(request.user)
        item = cart.items.get(id=cartitem_id)

        quantity = int(request.data.get('quantity'))
        item.quantity = quantity

        item.save()
        return Response(CartSerializer(cart, context={'request': request}).data, status=status.HTTP_200_OK)

    def delete(self, request: Request, cartitem_id: None):
        cart = self.get_cart(request.user)
        cart.items.get(id=cartitem_id).delete()
        return Response({"data": "با موفقیت حذف شد"}, status=status.HTTP_200_OK)


class DeleteAllCartItems(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def delete(self, request: Request):
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        return Response({"data": "با موفقیت حذف شدند"}, status=status.HTTP_200_OK)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        if self.request.user.role != 'admin':
            return Order.objects.filter(user=self.request.user).order_by("-created_at")
        return Order.objects.all()


class OrderDetailView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request, order_id: int):
        order = Order.objects.filter(user=request.user, pk=order_id).get()
        order_serializer = OrderSerializer(order, context={'request': request})
        return Response(order_serializer.data, status.HTTP_200_OK)
    def patch(self, request, order_id: int):
        try:
            order = Order.objects.filter(user=request.user, pk=order_id).get()
            order_serializer = OrderSerializer(order, context={'request': request})
            order.status = request.data.get('status')
            order.save()
            return Response({"data": order_serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': json.dumps(e)}, status=status.HTTP_400_BAD_REQUEST)


    

class CategoryBannerView(APIView):
    def get(self, request: Request):
        cat_banner = CategoryBanner.objects.all()
        banner_serializer = CategoryBannerSerializer(cat_banner, many=True, context={'request': request})
        return Response({'data': banner_serializer.data}, status.HTTP_200_OK)


class SingleCategoryView(APIView):
    def get(self, request: Request, category_id):
        category = ProductCategory.objects.get(pk=category_id)
        category_serializer = CategorySerializer(category)
        return Response({'data': category_serializer.data}, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request: Request):
    user = request.user
    payment_method = request.data.get("payment_method")
    if payment_method == "wallet":
        payment_method = Payment.PaymentMethod.Wallet
    elif payment_method == "cod":
        payment_method = Payment.PaymentMethod.COD
    cart = Cart.objects.get(user=user)
    total_cart_value = 0
    for item in cart.items.all():
        total_cart_value += int(item.product.price) * item.quantity
    if payment_method == Payment.PaymentMethod.Wallet and user.wallet.balance < total_cart_value:
        return Response({
            "error": "موجودی کیف پول کافی نیست!"
        })
    try:
        order = create_order(user)
        order_serializer = OrderSerializer(order)
        if payment_method == Payment.PaymentMethod.Wallet:
            balance = user.wallet.balance
            isInteger = (balance - total_cart_value) >= 0
            if isInteger:
                user.wallet.balance -= total_cart_value
                user.wallet.save()
                order.status = "paid"
                order.save()
                WalletTransaction.objects.create(
                    wallet=user.wallet,type="order", method="card",description="پرداخت سفارش از کیف پول",amount=total_cart_value)
        elif payment_method == Payment.PaymentMethod.COD:
            order.status = "pending"
            order.save()
        payment = Payment.objects.create(
            payment_method=payment_method,
            gateway='',
            order_id=order.id,
            is_successful=True,
            authority='',
        )
        payment.save()
        transaction = Transaction.objects.create(
            user=request.user,
            amount=total_cart_value,
            gateway='',
            status=Transaction.Status.SUCCESS,
            type=Transaction.Type.Order,
            description=payment_method
        )
        transaction.save()
        return Response({'data': order_serializer.data}, status.HTTP_200_OK)
    except Exception as err:
        return Response({"msg": "some error occured",
                          "error": str(err)}, status.HTTP_403_FORBIDDEN)


class PaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            order = create_order(user)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(order=order, gateway='zarinpal',
                                         payment_method=Payment.PaymentMethod.PaymentGateway)

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(order.total_price * 10),
            "callback_url": f"{settings.ZARINPAL_CALLBACK_URL}?order_id={order.id}",
            "description": f"پرداخت سفارش شماره {order.id}",
        }

        res = requests.post(settings.ZARINPAL_REQUEST_URL, json=data)
        result = res.json()

        print("ZARINPAL REQUEST RESULT:", result)

        if result.get("data") and result["data"].get("code") == 100:
            authority = result["data"]["authority"]
            payment.authority = authority
            payment.save()
            payment_url = f"{settings.ZARINPAL_STARTPAY_URL}{authority}"
            user.cart.items.all().delete()
            return Response({
                "orderId": order.id,
                "paymentUrl": payment_url
            }, status=status.HTTP_200_OK)

        return Response({
            "error": result.get("errors"),
            "raw": result
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerifyView(APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        authority = request.data.get("authority")
        status_param = request.data.get("status")

        try:
            payment = Payment.objects.get(order_id=order_id, authority=authority)
            order = payment.order
        except Payment.DoesNotExist:
            return Response({"detail": "Invalid payment"}, status=status.HTTP_404_NOT_FOUND)

        if status_param != 'OK':
            return Response({"detail": "Payment canceled by user"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(order.total_price) * 10,
            "authority": authority,
        }

        res = requests.post(settings.ZARINPAL_VERIFY_URL, json=data)
        result = res.json()

        if result.get("data") and result["data"].get("code") == 100:
            payment.is_successful = True
            payment.ref_id = result["data"]["ref_id"]
            payment.save()
            order.status = 'paid'
            order.save()

            Transaction.objects.create(
                user=request.user,
                status=Transaction.Status.SUCCESS,
                type=Transaction.Type.Order,
                description="پرداخت مستقیم سفارش",
                reference_id=payment.ref_id,
                gateway="زرین پال",
                amount=order.total_price
            )

            return Response({
                "success": True,
                "detail": "Payment successful",
                "ref_id": payment.ref_id,
                "order_id": order.id
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Payment failed", "result": result}, status=status.HTTP_400_BAD_REQUEST)


class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        return Response({"balance": wallet.balance})


class WalletTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = TransactionSerializer(wallet.transactions.all(), many=True)
        return Response({"transactions": serializer.data})


class WalletDepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        method = request.data.get("method", "card")

        if not amount or float(amount) <= 0:
            return Response({"error": "مبلغ نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = Wallet.objects.get(user=request.user)

        with transaction.atomic():
            wallet.balance += float(amount)
            wallet.save()
            WalletTransaction.objects.create(
                wallet=wallet,
                type="credit",
                method=method,
                amount=amount,
                description="شارژ کیف پول"
            )

        return Response({"message": "شارژ کیف پول موفقیت‌آمیز بود"})


class WalletWithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        method = request.data.get("method", "iban")

        if not amount or float(amount) <= 0:
            return Response({"error": "مبلغ نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = Wallet.objects.get(user=request.user)
        if wallet.balance < float(amount):
            return Response({"error": "موجودی کافی نیست"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            wallet.balance -= float(amount)
            wallet.save()
            WalletTransaction.objects.create(
                wallet=wallet,
                type="debit",
                method=method,
                amount=amount,
                description="برداشت وجه"
            )

        return Response({"message": "برداشت با موفقیت انجام شد"})


class WalletPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        gateway = request.data.get("gateway", "zarinpal")

        if not amount or float(amount) <= 0:
            return Response({"error": "مبلغ نامعتبر است"}, status=status.HTTP_400_BAD_REQUEST)

        # در اینجا مثلاً درخواست پرداخت زرین‌پال ساخته می‌شود
        payment_url = f"https://example.com/payment/start?amount={amount}&user={request.user.id}"

        return Response({"paymentUrl": payment_url})


class WalletPaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get("amount")

        if not amount or (float(amount) <= 0) or (float(amount) < 100):
            return Response({"message": "حداقل مبلغ ممکن 100 تومان میبشد."}, status=status.HTTP_400_BAD_REQUEST)

        wallet, _ = Wallet.objects.get_or_create(user=user)

        payment = WalletPayment.objects.create(wallet=wallet, amount=amount, gateway='zarinpal')

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(float(amount) * 10),
            "callback_url": f"{settings.ZARINPAL_WALLET_CALLBACK_URL}?payment_id={payment.id}",
            "description": f"شارژ کیف پول کاربر {user.phone if hasattr(user, 'phone') else user.username}",
        }

        res = requests.post(settings.ZARINPAL_REQUEST_URL, json=data)
        result = res.json()

        print("WALLET ZARINPAL REQUEST RESULT:", result)

        if result.get("data") and result["data"].get("code") == 100:
            authority = result["data"]["authority"]
            payment.authority = authority
            payment.save()
            payment_url = f"{settings.ZARINPAL_STARTPAY_URL}{authority}"
            return Response({
                "paymentUrl": payment_url,
                "paymentId": payment.id
            }, status=status.HTTP_200_OK)

        return Response({
            "error": result.get("errors"),
            "raw": result
        }, status=status.HTTP_400_BAD_REQUEST)


class WalletPaymentVerifyView(APIView):
    def post(self, request: Request):
        payment_id = request.data.get("payment_id")
        authority = request.data.get("authority")
        zarinpal_status = request.data.get("zarinpal_status")
        try:
            payment = WalletPayment.objects.get(id=payment_id, authority=authority)
            wallet = payment.wallet
        except WalletPayment.DoesNotExist:
            return Response({"detail": "Invalid payment"}, status=status.HTTP_404_NOT_FOUND)

        if zarinpal_status != 'OK':
            if payment:
                payment.is_successful = False
            return Response({"detail": "Payment canceled by user"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": int(float(payment.amount) * 10),
            "authority": authority,
        }

        res = requests.post(settings.ZARINPAL_VERIFY_URL, json=data)
        result = res.json()

        if result.get("data") and result["data"].get("code") == 100:
            payment.is_successful = True
            payment.ref_id = result["data"]["ref_id"]
            payment.save()
            payment.status = 'paid'
            payment.save()

            wallet.balance += payment.amount
            wallet.save()
            WalletTransaction.objects.create(
                wallet=wallet,
                type="credit",
                method="card",
                amount=payment.amount,
                description=f"شارژ موفق کیف پول (رسید {payment.ref_id})"
            )
            Transaction.objects.create(
                user=request.user,
                amount=payment.amount,
                gateway='زرین پال',
                description="شارژ کیف پول",
                status=Transaction.Status.SUCCESS,
                type=Transaction.Type.WalletCharge,
                reference_id=payment.ref_id,
            )

            # Redirect to frontend success page
            return Response({
                "success": True,
            })

        return Response({
            "success": False,
        })
