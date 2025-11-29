from django.urls import path
from . import views

urlpatterns = [
    # routes related to products
    path("search-product", views.FilteredProductsView.as_view()),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/description', views.ProductDescriptionView.as_view(), name='product-detail'),
    path('products/<int:product_id>/specs', views.ProductPropertyView.as_view(), name='product-detail'),
    path('products/<int:product_id>/comments', views.AddComment.as_view(), name='add-product-comment'),
    path('products/<int:product_id>/comments/approved', views.ApprovedCommentsView.as_view()),
    
    # routes for category
    path('category/<int:category_id>', views.SingleCategoryView.as_view()),
    
    # routes related to cart and order
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/clear', views.DeleteAllCartItems.as_view(), name='cart'),
    path('cart/<int:cartitem_id>', views.CartView.as_view(), name='cart-delete'),
    path('orders/', views.OrderListView.as_view(), name='order-list-create'),
    path('orders/<int:order_id>', views.OrderDetailView.as_view(), name='order-detail'),

    
    # routes for payment
    path('checkout/', views.checkout, name='checkout'),
    path('payments/zarinpal/request/', views.PaymentRequestView.as_view(), name='payment-request'),
    path('payments/zarinpal/verify/', views.PaymentVerifyView.as_view(), name='payment-verify'),
    
    # routes for wallet
    path("wallet/balance/", views.WalletBalanceView.as_view(), name="wallet-balance"),
    path("wallet/transactions/", views.WalletTransactionsView.as_view(), name="wallet-transactions"),
    path("wallet/deposit/", views.WalletDepositView.as_view(), name="wallet-deposit"),
    path("wallet/withdraw/", views.WalletWithdrawView.as_view(), name="wallet-withdraw"),
    path("wallet/payment/", views.WalletPaymentRequestView.as_view(), name="wallet-payment"),
    path("wallet/verify/", views.WalletPaymentVerifyView.as_view(), name="wallet-verify"),
]