from rest_framework import serializers
from .models import BannerImages, SiteSetting, FooterLink, FooterLinkBox, TrustSymbols, Header


class BannerImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = BannerImages
        fields = '__all__'


class HeaderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Header
        fields = '__all__'


class SiteLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = ['site_logo']


class SiteAboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = ['title', 'text', 'imageurl']


class SiteSettingSerializer(serializers.ModelSerializer):
    # site_logo = serializers.ImageField(use_url=True)
    # about_us_logo = serializers.ImageField(use_url=True)

    class Meta:
        model = SiteSetting
        fields = ['id', 'phone', 'email', 'address']


class FooterLinkBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLinkBox
        fields = '__all__'


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = '__all__'


class TrustSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustSymbols
        fields = '__all__'
