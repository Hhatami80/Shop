from django.urls import path
from . import views

urlpatterns = [
    path('change-password', views.PasswordUpdateView.as_view(), name='change-password'),
    path('user/profile/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('user/bank-accounts/', views.BankInformationView.as_view(), name='bank-account'),
    path('user/bank-accounts-delete/<int:bank_id>', views.BankInfoDeleteView.as_view(), name='bank-account-delete'),
    path('locations/provinces/', views.ProvinceListView.as_view(), name='province-list'),
    path('locations/cities/', views.CityListView.as_view(), name='city-list'),
    path('user/addresses/', views.AddressListCreateView.as_view(), name='address-list'),
    path('user/addresses/<int:pk>', views.AddressDetailView.as_view(), name='address-detail'),
]
