from django.urls import path
from . import views

urlpatterns = [
    # path('product-detail/<path:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/description', views.ProductDescriptionView.as_view(), name='product-detail'),
    path('products/<int:product_id>/specs', views.ProductPropertyView.as_view(), name='product-detail'),
    path('products/<int:product_id>/comments', views.AddComment.as_view(), name='add-product-comment'),
    path('products/<int:product_id>/comments/approved', views.ApprovedCommentsView.as_view()),
    # path('products/<int:pk>/favorites', views.ToggleFavoriteView.as_view(), name='toggle-favorite'),
    # path('favorites', views.FavoriteListView.as_view(), name='favorite-list'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/clear', views.DeleteAllCartItems.as_view(), name='cart'),
    path('cart/<int:cartitem_id>', views.CartView.as_view(), name='cart-delete'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('banners', views.CategoryBannerView.as_view()),
    path('category/<int:category_id>', views.SingleCategoryView.as_view()),
    path('checkout/', views.checkout, name='checkout'),
]