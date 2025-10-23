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


class ProductView(APIView):
    def get(self, request: Request):
        product = Product.objects.prefetch_related('properties')
        product_serializer = ProductSerializer(product, many=True, context={'request': request})
        discounted_products = Product.objects.exclude(discount=None)
        discounted_serializer = ProductMainPageSerializer(discounted_products, many=True, context={'request': request})
        new_products = Product.objects.order_by('-id')[:6]
        new_product_serializer = ProductMainPageSerializer(new_products, many=True, context={'request': request})
        return Response({
            'products': product_serializer.data,
            'discounted_product': discounted_serializer.data,
            'new_products': new_product_serializer.data,
        }, status.HTTP_200_OK)


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
        products = Product.objects.filter(is_done=False)
        random = Product.objects.get(pk=1)
        best_seller = BestSellerSerializer(products, many=True, context={'request': request})
        return Response({'products': best_seller.data,
                         'image': request.build_absolute_uri(random.image.url) if random.image else None},
                        status.HTTP_200_OK)


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
