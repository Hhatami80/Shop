from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from site_module.models import BannerImages, SiteSetting, FooterLink, FooterLinkBox, TrustSymbols, Header
from site_module.serializers import BannerImageSerializer, SiteSettingSerializer, FooterLinkSerializer, \
    FooterLinkBoxSerializer, TrustSymbolSerializer, HeaderSerializer, SiteLogoSerializer, SiteAboutUsSerializer
from product_module.models import Product, ProductCategory, Brand
from product_module.serializers import CategorySerializer, ProductSerializer, BrandSerializer
from .serializers import ProductMainPageSerializer, BestSellerSerializer
from django.db.models import Q


# Create your views here.

class BannerView(APIView):
    def get(self, request: Request):
        banner = BannerImages.objects.all()
        banner_serializer = BannerImageSerializer(banner, many=True, context={'request': request})
        return Response({'banner': banner_serializer.data}, status.HTTP_200_OK)

class PooshineProductsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request: Request):
        pooshine = Product.objects.filter(category__title="پوشینه", is_active=True).all()
        serializer = ProductSerializer(pooshine, many=True, context={'request': request})
        return Response(serializer.data)
    
class ProductView(APIView):
    def get(self, request: Request):
        try:
            products_query = (Product.objects
                              .select_related('category')
                              .prefetch_related('images')
                              .filter(is_active=True, is_done=False))

            available_products = products_query.filter(~Q(category__title="پوشینه")).all()
            product_serializer = ProductSerializer(available_products, many=True, context={'request': request})
            discounted_products = available_products
            discounted_products_serializer = ProductSerializer(discounted_products, many=True, context={'request': request})
            new_products = products_query.filter(~Q(category__title="پوشینه")).order_by('-created_date').all()
            new_products_serializer = ProductSerializer(new_products, many=True, context={'request': request})
            pooshineh_products = products_query.filter(category__title__contains="پوشینه").all()
            pooshineh_serializer = ProductSerializer(pooshineh_products, many=True, context={'request': request})
            return Response({
                'products': product_serializer.data,
                'discounted_products': discounted_products_serializer.data,
                'new_products': new_products_serializer.data,
                'pooshineh': pooshineh_serializer.data,
                
            }, status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                'products': [],
                'discounted_products': [],
                'new_products': [],
            }, status.HTTP_404_NOT_FOUND)





class ProductCategoryView(APIView):
    def get(self, request: Request):
        categories = ProductCategory.objects.all()
        category_serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response({
            'categories': category_serializer.data,
        }, status.HTTP_200_OK)


class ProductBrandView(APIView):
    def get(self, request: Request):
        brands = Brand.objects.all()
        brand_serializer = BrandSerializer(brands, many=True, context={'request': request})
        return Response({
            'brands': brand_serializer.data,
        }, status.HTTP_200_OK)


class SiteSettingView(APIView):
    def get(self, request: Request):
        # --- Contact Section ---
        site_setting, _ = SiteSetting.objects.get_or_create(
            defaults={
                'site_name': 'سرینه',
                'phone': '۰۲۱-۱۲۳۴۵۶۷۸',
                'email': 'info@shop.ir',
                'address': 'تهران، خیابان انقلاب، پلاک ۱۲۳',
                'text': 'به فروشگاه ما خوش آمدید! بهترین درب‌ها را با بهترین قیمت ارائه می‌دهیم.'
            }
        )
        site_serializer = SiteSettingSerializer(site_setting, context={'request': request})

        # --- Footer Link Boxes ---
        footer_linkbox_1, _ = FooterLinkBox.objects.get_or_create(
            pk=1,
            defaults={'title': 'لینک‌های مفید'}
        )
        footer_linkbox_2, _ = FooterLinkBox.objects.get_or_create(
            pk=2,
            defaults={'title': 'سرویس‌ها'}
        )

        # --- Footer Links (Box 1) ---
        if footer_linkbox_1.footer_link.exists():
            links = footer_linkbox_1.footer_link.all()
        else:
            links = []
        links_serializer = FooterLinkSerializer(links, many=True)

        # --- Services Links (Box 2) ---
        if footer_linkbox_2.footer_link.exists():
            services = footer_linkbox_2.footer_link.all()
        else:
            services = []
        services_serializer = FooterLinkSerializer(services, many=True)

        # --- Badges Section ---
        if TrustSymbols.objects.exists():
            badges = TrustSymbols.objects.all()
        else:
            badges = []
        badge_serializer = TrustSymbolSerializer(badges, many=True, context={'request': request})

        # --- Response ---
        return Response({
            'contact': site_serializer.data,
            'links': links_serializer.data,
            'services': services_serializer.data,
            'badges': badge_serializer.data,
        }, status=status.HTTP_200_OK)


class HeaderListView(APIView):
    def get(self, request: Request):
        headers = Header.objects.all().order_by('order')
        header_serializer = HeaderSerializer(headers, many=True)
        return Response({'header': header_serializer.data}, status.HTTP_200_OK)


class GetLogoView(APIView):
    def get(self, request: Request):
        site_setting = SiteSetting.objects.first()
        site_serializer = SiteLogoSerializer(site_setting, context={'request': request})
        return Response({'data': site_serializer.data}, status.HTTP_200_OK)


class AboutUsMainView(APIView):
    def get(self, request: Request):
        about_us = SiteSetting.objects.first()
        about_us_serializer = SiteAboutUsSerializer(about_us, context={'request': request})
        return Response({'data': about_us_serializer.data}, status.HTTP_200_OK)

# class SpecialProductsView(APIView):
#     def get(self, request: Request):
#         products = Product.objects.exclude(discount=None)
#         product_serializer = ProductMainPageSerializer(products, many=True, context={'request': request})
#         return Response({'data': product_serializer.data}, status.HTTP_200_OK)


class BestSellerView(APIView):
    def get(self, request: Request):
        product = Product.objects.filter(is_active=True, is_done=False).filter(~Q(category__title="پوشینه")).order_by('-created_date').all()
        serializer = BestSellerSerializer(product, many=True, context={'request': request})
        return Response({'bestsellers': serializer.data})


class ProductSearchView(APIView):
    def get(self, request: Request):
        search_query = request.query_params.get('search', '').strip()
        product = Product.objects.all()

        if search_query:
            product = Product.objects.filter(
                Q(title__icontains=search_query)
            )
        product_serializer = ProductSerializer(product, many=True)

        return Response({'data': product_serializer.data}, status.HTTP_200_OK)
