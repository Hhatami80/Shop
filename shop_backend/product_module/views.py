from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, ProductGallery, ProductComment, Cart, CartItem, ProductRating, OrderItem, Order, \
    CategoryBanner, ProductCategory
from .serializers import ProductSerializer, ProductGallerySerializer, ProductCommentSerializer, \
    ProductDescriptionSerializer, ProductPropertySerializer, CartItemSerializer, CartSerializer, \
    ProductRatingSerializer, OrderSerializer, CategoryBannerSerializer, CategorySerializer
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from .services import create_order


# Create your views here.

class ProductDetailView(APIView):
    def get(self, request: Request, product_id):
        product = Product.objects.get(pk=product_id)
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
        product = Product.objects.get(id=product_id)
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


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'admin':
            return Order.objects.filter(user=self.request.user)
        return Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


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
    order = create_order(user)
    order_serializer = OrderSerializer(order)
    return Response({'data': order_serializer.data}, status.HTTP_200_OK)
