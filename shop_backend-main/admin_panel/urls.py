from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('admin/orders', views.OrderAdminViewSet, basename='admin-orders')

urlpatterns = [
    # Product CRUD Api
    path("admin/products", views.AdminProductsView.as_view(), name='list_products'),
    path('product-add', views.AddProductView.as_view(), name='add-product'),
    path('product-delete/<int:product_id>', views.DeleteProductView.as_view(), name='delete-product'),
    path('product-edit/<int:product_id>', views.UpdateProductView.as_view(), name='update-product'),
    # Product Property CRUD Api
    path('property-add', views.AddPropertyView.as_view(), name='add-property'),
    path('property-delete/<int:property_id>', views.DeletePropertyView.as_view(), name='delete-property'),
    path('property-edit/<int:property_id>', views.UpdatePropertyView.as_view(), name='update-product'),
    # Category CRUD Api
    path('category-add', views.AddCategoryView.as_view(), name='add-category'),
    path('category-delete/<int:category_id>', views.DeleteCategoryView.as_view(), name='delete-category'),
    path('category-edit/<int:category_id>', views.UpdateCategoryView.as_view(), name='update-category'),
    # Brand CRUD Api
    path('brands-add', views.AddBrandView.as_view(), name='add-brand'),
    path('brands-delete/<int:brand_id>', views.DeleteBrandView.as_view(), name='delete-brand'),
    path('brands-edit/<int:brand_id>', views.UpdateBrandView.as_view(), name='update-brand'),
    # Banner CRUD Api
    path('feature-section-update/', views.AddBannerView.as_view(), name='add-banner'),
    # path('banner-delete/<int:banner_id>', views.DeleteBannerView.as_view(), name='delete-banner'),
    # path('banner-edit/<int:banner_id>', views.UpdateBannerView.as_view(), name='update-banner'),
    # Comment CRUD Api
    path('admin/comments', views.CommentsAllDisplay.as_view(), name='display-comment'),
    path('admin/comments/<int:comment_id>', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('admin/comments/bulk-delete', views.DeleteCommentBulkView.as_view(), name='delete-bulk-comment'),
    path('admin/comments/<int:comment_id>/approve', views.ApproveCommentView.as_view(), name='approve-comment'),
    path('admin/comments/bulk-approve', views.ApproveCommentBulkView.as_view(), name='approve-bulk-comment'),
    # Header Items CRUD Api
    path('header/', views.UpdateDeleteHeaderView.as_view(), name='update-delete-header'),
    path('upload-logo/', views.SetLogoView.as_view(), name='site-logo'),
    # Footer Items CRUD Api
    path('admin/footer/', views.FooterUpdateView.as_view(), name='add-link'),
    # About Us Main Page API
    path('aboutus/', views.UpdateAboutUsMainView.as_view(), name='about-us-main'),
    # User API
    path('users', views.ListUserView.as_view(), name='user-admin'),
    path('users/<int:user_id>', views.UpdateDeleteUserView.as_view(), name='user-update-delete'),
    # Article CRUD API
    path('articles', views.AddArticleView.as_view(), name='add-article'),
    path('articles-edit/<int:article_id>', views.UpdateDeleteArticleView.as_view(), name='edit-article'),
    path('articles-delete/<int:article_id>', views.UpdateDeleteArticleView.as_view(), name='delete-article'),
    #
    path('', include(router.urls)),

]
