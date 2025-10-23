from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from product_module.models import Product, ProductProperty, ProductCategory, Brand, ProductComment, CategoryBanner
from product_module.serializers import ProductSerializer, ProductPropertySerializer, CategorySerializer, \
    BrandSerializer, ProductCommentSerializer, CategoryBannerSerializer
from site_module.serializers import BannerImageSerializer, FooterLinkSerializer, TrustSymbolSerializer, \
    HeaderSerializer, SiteSettingSerializer, SiteLogoSerializer, SiteAboutUsSerializer
from site_module.models import BannerImages, FooterLinkBox, TrustSymbols, FooterLink, Header, SiteSetting
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import math
from rest_framework.parsers import MultiPartParser, FormParser
from account_module.models import User
from account_module.serializers import UserSerializer, UserAdminSerializer
from article_module.models import Article
from article_module.serializers import ArticleSerializer


# Create your views here.


# region Product
class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        category = ProductCategory.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return Response({'categories': category_serializer.data}, status.HTTP_200_OK)

    def post(self, request: Request):
        product_serializer = ProductSerializer(data=request.data, context={'request': request})
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'data': product_serializer.data}, status.HTTP_201_CREATED)
        return Response({'errors': product_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, category_id: int):
        try:
            product = Product.objects.get(pk=category_id)
            return product
        except ProductCategory.DoesNotExist:
            return Response({'errors': 'محصولی وجود ندارد'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, product_id):
        product = self.get_object(product_id)
        product.delete()
        return Response({'data': 'محصول با موفقیت حذف شد'}, status.HTTP_204_NO_CONTENT)


class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            return product
        except Product.DoesNotExist:
            return Response({'errors': 'محصولی وجود ندارد'}, status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, product_id):
        product = self.get_object(product_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'data': 'اطلاعات ویرایش شد'}, status.HTTP_201_CREATED)

        return Response({'errors': product_serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion

# region Product Property

class AddPropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        property_serializer = ProductPropertySerializer(data=request.data)
        if property_serializer.is_valid():
            property_serializer.save()
            return Response({'data': property_serializer.data}, status.HTTP_201_CREATED)

        return Response({'errors': property_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class DeletePropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, property_id):
        try:
            product_property = ProductProperty.objects.get(pk=property_id)
            return product_property
        except ProductProperty.DoesNotExist:
            return Response({'errors': 'همچین ویژگی محصولی وجود ندارد'})

    def delete(self, request: Request, property_id):
        product_property = self.get_object(property_id)
        product_property.delete()
        return Response({'data': 'ویژگی محصول با موفقیت حذف شد'}, status.HTTP_204_NO_CONTENT)


class UpdatePropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, property_id):
        try:
            product_property = ProductProperty.objects.get(pk=property_id)
            return property
        except ProductProperty.DoesNotExist:
            return Response({'errors': 'همچین ویژگی محصولی وجود ندارد'})

    def put(self, request: Request, property_id):
        product_property = self.get_object(property_id)
        property_serializer = ProductPropertySerializer(product_property, data=request.data, partial=True)
        if property_serializer.is_valid():
            property_serializer.save()
            return Response({'data': 'اطلاعات ویرایش شد'}, status.HTTP_201_CREATED)
        return Response({'errors': property_serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion

# region Category

class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response({'data': category_serializer.data}, status.HTTP_201_CREATED)
        return Response({'errors': category_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, category_id: int):
        try:
            category = ProductCategory.objects.get(pk=category_id)
            return category
        except ProductCategory.DoesNotExist:
            return Response({'errors': 'دسته بندی وجود ندارد'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, category_id: int):
        category = self.get_object(category_id)
        category.delete()
        return Response({'data': 'دسته بندی با موفقیت حذف شد'}, status.HTTP_204_NO_CONTENT)


class UpdateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, category_id: int):
        try:
            category = ProductCategory.objects.get(pk=category_id)
            return category
        except ProductCategory.DoesNotExist:
            return Response({'errors': 'دسته بندی وجود ندارد'}, status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, category_id):
        category = self.get_object(category_id)
        category_serializer = CategorySerializer(category, context={'request': request})
        return Response({'data': category_serializer.data}, status.HTTP_200_OK)

    def put(self, request: Request, category_id):
        category = self.get_object(category_id)
        category_serializer = CategorySerializer(category, data=request.data, partial=True)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response({'data': 'اطلاعات ویرایش شد'}, status.HTTP_201_CREATED)
        return Response({'errors': category_serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion

# region Brand
class AddBrandView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        brand_serializer = BrandSerializer(data=request.data)
        if brand_serializer.is_valid():
            brand_serializer.save()
            return Response({'data': brand_serializer.data}, status.HTTP_201_CREATED)
        return Response({'errors': brand_serializer.errors}, status.HTTP_400_BAD_REQUEST)


class DeleteBrandView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, brand_id):
        try:
            brand = Brand.objects.get(pk=brand_id)
            return brand
        except Brand.DoesNotExist:
            return Response({'errors': 'برند وجود ندارد'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, brand_id):
        brand = self.get_object(brand_id)
        brand.delete()
        return Response({'data': 'برند با موفقیت حذف شد'}, status.HTTP_204_NO_CONTENT)


class UpdateBrandView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, brand_id):
        try:
            brand = Brand.objects.get(pk=brand_id)
            return brand
        except Brand.DoesNotExist:
            return Response({'errors': 'برند وجود ندارد'}, status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, brand_id):
        brand = self.get_object(brand_id)
        brand_serializer = BrandSerializer(brand, data=request.data, partial=True)
        if brand_serializer.is_valid():
            brand_serializer.save()
            return Response({'data': 'اطلاعات ویرایش شد'}, status.HTTP_201_CREATED)
        return Response({'errors': brand_serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion

# region Banner

class AddBannerView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        banner = BannerImages.objects.first()
        serializer = BannerImageSerializer(banner, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion


# region Comment

def search_comments(query):
    words = query.split()
    q = Q()
    for word in words:
        q &= Q(text__icontains=word)  # AND condition
    return ProductComment.objects.filter(q)


class CommentsAllDisplay(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        comment_status = request.query_params.get('status')
        search_query = request.query_params.get('search', '').strip()

        try:
            page = int(request.query_params.get('page', 1))
            _ = request.query_params.get('totalPages')
            per_page = int(request.query_params.get('per_page', 5))
        except ValueError:
            return Response({'errors': 'page یا perpage باید عدد باشند'}, status=status.HTTP_400_BAD_REQUEST)

        comments = ProductComment.objects.all()

        if comment_status == 'approved':
            comments = comments.filter(is_approved=True)
        elif comment_status == 'unapproved':
            comments = comments.filter(is_approved=False)
        elif comment_status == 'all':
            pass
        elif comment_status:
            return Response({'errors': 'مقدار وضعیت نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        # if search_query:
        #     comments = comments.filter(
        #         Q(text__icontains=search_query)
        #     )
        words = search_query.split()
        q = Q()
        for word in words:
            q &= Q(text__icontains=word)  # AND condition
        comments = comments.filter(q)

        total_comments = comments.count()
        total_pages = math.ceil(total_comments / per_page)

        start = (page - 1) * per_page
        end = start + per_page
        paginated_comments = comments[start:end]

        serializer = ProductCommentSerializer(paginated_comments, many=True)

        return Response({
            'comments': serializer.data,
            'comment_count': total_comments,
            'totalPages': total_pages,
            'page': page,
            'perPage': per_page
        }, status=status.HTTP_200_OK)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, comment_id):
        try:
            comment = ProductComment.objects.get(pk=comment_id)
            return comment
        except ProductComment.DoesNotExist:
            return Response({'errors': 'کامنت وجود ندارد'}, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, comment_id):
        comment = self.get_object(comment_id)
        comment.delete()
        return Response({'data': 'کامنت با موفقیت حذف شد'}, status.HTTP_204_NO_CONTENT)


class DeleteCommentBulkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        comment_ids = request.data.get('ids', [])

        if not comment_ids or not isinstance(comment_ids, list):
            return Response({'errors': 'لیست شناسه‌های کامنت ارسال نشده یا نادرست است'}, status.HTTP_400_BAD_REQUEST)

        comments = ProductComment.objects.filter(id__in=comment_ids)
        deleted_count = comments.count()

        if deleted_count == 0:
            return Response({'errors': 'کامنتی برای حذف یافت نشد یا اجازه حذف ندارید.'}, status.HTTP_404_NOT_FOUND)

        comments.delete()
        return Response({'data': f'{deleted_count}کامنت با موفقیت حذف شد'}, status.HTTP_204_NO_CONTENT)


class ApproveCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, comment_id):
        try:
            comment = ProductComment.objects.get(pk=comment_id)
            comment.is_approved = True
            comment.save()
            return Response({'data': 'کامنت تایید شد'}, status.HTTP_200_OK)
        except ProductComment.DoesNotExist:
            return Response({'errors': 'کامنت مورد نظر وجود ندارد'}, status.HTTP_400_BAD_REQUEST)


class ApproveCommentBulkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        comment_ids = request.data.get('ids', [])

        if not comment_ids or not isinstance(comment_ids, list):
            return Response({'errors': 'لیست شناسه‌های کامنت ارسال نشده یا نادرست است'}, status.HTTP_400_BAD_REQUEST)

        comments = ProductComment.objects.filter(id__in=comment_ids)
        approved_count = comments.count()

        if approved_count == 0:
            return Response({'errors': 'کامنتی برای حذف یافت نشد یا اجازه حذف ندارید.'}, status.HTTP_404_NOT_FOUND)

        comments.update(is_approved=True)

        return Response({'data': f'{approved_count} کامنت تایید شد'}, status.HTTP_200_OK)


# endregion

# region Header
class UpdateDeleteHeaderView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        incoming_items = request.data.get('header', [])

        existing_items = Header.objects.all()
        incoming_ids = [item.get('id') for item in incoming_items if 'id' in item]

        # delete items not in request
        Header.objects.exclude(id__in=incoming_ids).delete()

        for index, item_data in enumerate(incoming_items):
            item_id = item_data.get('id', None)
            item_data['order'] = index  # Set order based on position in list

            if item_id:
                try:
                    menu_item = Header.objects.get(id=item_id)
                    serializer = HeaderSerializer(menu_item, data=item_data)
                    if serializer.is_valid():
                        serializer.save()
                except Header.DoesNotExist:
                    serializer = HeaderSerializer(data=item_data)
                    if serializer.is_valid():
                        serializer.save()
            else:
                serializer = HeaderSerializer(data=item_data)
                if serializer.is_valid():
                    serializer.save()

        return Response({"message": "Menu updated successfully"}, status=status.HTTP_200_OK)


class SetLogoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request: Request):
        site_setting = SiteSetting.objects.first()
        site_serializer = SiteLogoSerializer(site_setting, context={'request': request})
        return Response({'data': site_serializer.data}, status.HTTP_200_OK)

    def put(self, request: Request):
        site_setting = SiteSetting.objects.first()
        site_serializer = SiteLogoSerializer(site_setting, data=request.data, partial=True,
                                             context={'request': request})
        if site_serializer.is_valid():
            site_serializer.save()
            return Response({'data': site_serializer.data}, status.HTTP_200_OK)
        return Response({'errors': site_serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion

# region Footer
class FooterUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        site_setting = SiteSetting.objects.first()
        site_serializer = SiteSettingSerializer(site_setting, context={'request': request})
        footer_linkbox_1 = FooterLinkBox.objects.get(pk=1)
        footer_linkbox_2 = FooterLinkBox.objects.get(pk=2)
        links = footer_linkbox_1.footer_link.all()
        services = footer_linkbox_2.footer_link.all()
        links_serializer = FooterLinkSerializer(links, many=True)
        services_serializer = FooterLinkSerializer(services, many=True)
        badge = TrustSymbols.objects.all()
        badge_serializer = TrustSymbolSerializer(badge, many=True, context={'request': request})
        return Response(
            {'contact': site_serializer.data, 'badges': badge_serializer.data, 'links': links_serializer.data,
             'services': services_serializer.data}, status.HTTP_200_OK)

    def put(self, request: Request):
        data = request.data

        # Contact Section (SiteSetting)
        contact_data = data.get('contact')
        if contact_data:
            site_setting = SiteSetting.objects.first()
            serializer = SiteSettingSerializer(site_setting, data=contact_data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Links Section (FooterLink)
        links_data = data.get('links', [])
        if links_data:
            incoming_ids = [item.get('id') for item in links_data if 'id' in item]
            FooterLink.objects.exclude(id__in=incoming_ids).delete()

            footer_linkbox_1 = FooterLinkBox.objects.get(pk=1)

            for item in links_data:
                if not isinstance(item, dict):
                    continue

                item_id = item.get('id')
                if item_id:
                    instance = FooterLink.objects.filter(id=item_id).first()
                    serializer = FooterLinkSerializer(instance, data=item, partial=True)
                else:
                    item['footer_link_box'] = footer_linkbox_1.id
                    serializer = FooterLinkSerializer(data=item)

                if serializer.is_valid():
                    serializer.save()
                else:
                    print('LINK CREATE ERROR:', serializer.errors)

        # Services Section
        services_data = data.get('services', [])
        if services_data:
            incoming_ids = [item.get('id') for item in services_data if 'id' in item]
            FooterLink.objects.exclude(id__in=incoming_ids).filter(
                footer_link_box__title__icontains='سرویس'
            ).delete()

            footer_linkbox_2 = FooterLinkBox.objects.get(pk=2)

            for item in services_data:
                if not isinstance(item, dict):
                    continue

                item_id = item.get('id')
                if item_id:
                    instance = FooterLink.objects.filter(id=item_id).first()
                    serializer = FooterLinkSerializer(instance, data=item, partial=True)
                else:
                    item['footer_link_box'] = footer_linkbox_2.id
                    serializer = FooterLinkSerializer(data=item)

                if serializer.is_valid():
                    serializer.save()
                else:
                    print('SERVICE CREATE ERROR:', serializer.errors)

        # Badges Section (TrustSymbols)
        badges_data = data.get('badges', [])
        if badges_data:
            incoming_ids = [item.get('id') for item in badges_data if 'id' in item]
            TrustSymbols.objects.exclude(id__in=incoming_ids).delete()

            for item in badges_data:
                item_id = item.get('id')
                image = item.get('image')

                if not image:
                    continue

                if item_id:
                    instance = TrustSymbols.objects.filter(id=item_id).first()
                    serializer = TrustSymbolSerializer(instance, data=item, partial=True)
                else:
                    serializer = TrustSymbolSerializer(data=item)

                if serializer.is_valid():
                    serializer.save()

        return Response({"message": "Footer updated successfully"}, status=status.HTTP_200_OK)


# endregion

# region About Us Main Page

class UpdateAboutUsMainView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        about_us = SiteSetting.objects.first()
        serializer = SiteAboutUsSerializer(about_us, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status.HTTP_400_BAD_REQUEST)


# endregion

# region Users

class ListUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        users = User.objects.all()
        user_serializer = UserAdminSerializer(users, many=True, context={'request': request})
        return Response({'data': user_serializer.data}, status.HTTP_200_OK)


class UpdateDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response({'data': 'کاربر با موفقیت حذف شد.'}, status.HTTP_204_NO_CONTENT)


# endregion

# region Article

class AddArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        articles = Article.objects.all()
        article_serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response({'articles': article_serializer.data}, status.HTTP_200_OK)

    def post(self, request: Request):
        article_serializer = ArticleSerializer(data=request.data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response({'data': 'مقاله با موفقیت اضافه شد'}, status.HTTP_200_OK)
        return Response({'errors': article_serializer.data}, status.HTTP_400_BAD_REQUEST)


class UpdateDeleteArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, article_id):
        articles = Article.objects.get(pk=article_id)
        article_serializer = ArticleSerializer(articles, context={'request': request})
        return Response({'articles': article_serializer.data}, status.HTTP_200_OK)

    def put(self, request: Request, article_id):
        articles = Article.objects.get(pk=article_id)
        article_serializer = ArticleSerializer(articles, data=request.data, partial=True)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response({'data': 'مقاله با موفقیت آپدیت شد'}, status.HTTP_200_OK)

        return Response({'errors': article_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, article_id):
        articles = Article.objects.get(pk=article_id)
        articles.delete()
        return Response({'data': 'مقاله با موفقیت حذف شد'}, status.HTTP_200_OK)


# endregion

# region CategoryBanner

class CategoryBannerView(APIView):
    def post(self, request: Request):
        banner_serializer = CategoryBannerSerializer(data=request.data)
        if banner_serializer.is_valid():
            banner_serializer.save()
            return Response({'data': 'بنر دسته بندی با موفقیت اضافه شد'}, status.HTTP_200_OK)
        return Response({'errors': banner_serializer.data}, status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, banner_id):
        cat_banner = CategoryBanner.objects.get(pk=banner_id)
        banner_serializer = CategoryBannerSerializer(cat_banner, context={'request': request})
        return Response({'category_banner': banner_serializer.data}, status.HTTP_200_OK)

    def put(self, request: Request, banner_id):
        cat_banner = CategoryBanner.objects.get(pk=banner_id)
        banner_serializer = CategoryBannerSerializer(cat_banner, data=request.data, partial=True)
        if banner_serializer.is_valid():
            banner_serializer.save()
            return Response({'data': 'بنر دسته بندی با موفقیت آپدیت شد'}, status.HTTP_200_OK)

        return Response({'errors': banner_serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, banner_id):
        cat_banner = CategoryBanner.objects.get(pk=banner_id)
        cat_banner.delete()
        return Response({'data': 'بنر دسته بندی با موفقیت حذف شد'}, status.HTTP_200_OK)


# endregion
