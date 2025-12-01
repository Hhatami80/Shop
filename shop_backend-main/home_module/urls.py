from django.urls import path
from . import views

urlpatterns = [
    path('feature-section', views.BannerView.as_view(), name='banner-image-view'),
    path('products', views.ProductView.as_view(), name='product-view'),
    path('category', views.ProductCategoryView.as_view(), name='category-view'),
    path('brands', views.ProductBrandView.as_view(), name='brand-view'),
    path('header', views.HeaderListView.as_view(), name='header'),
    path('upload-logo1', views.GetLogoView.as_view()),
    path('footer', views.SiteSettingView.as_view(), name='footer'),
    path('aboutus', views.AboutUsMainView.as_view(), name='about-us-main'),
    path('products/bestsellers', views.BestSellerView.as_view(), name='best-seller'),
    path('products/pooshine', views.PooshineProductsView.as_view(), name='pooshine-products'),
    # path('products/special-products', views.SpecialProductsView.as_view(), name='special-products'),
    path('products/search/', views.ProductSearchView.as_view(), name='product-search'),
]