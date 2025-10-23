from django.urls import path
from . import views

urlpatterns = [
    path('change-password', views.PasswordUpdateView.as_view(), name='change-password'),
    path('user/profile/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('user/bank-accounts/', views.BankInformationView.as_view(), name='bank-account'),
    path('user/addresses/', views.AddressInformationView.as_view(), name='address-info'),
]