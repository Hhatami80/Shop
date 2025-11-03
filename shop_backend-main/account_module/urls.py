from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.RegisterView.as_view(), name='register-view'),
    path('sign-in', views.LoginView.as_view(), name='login-view'),
    path('sign-out/', views.LogoutView.as_view(), name='logout-view'),
    path('verify-otp', views.VerifyOTPView.as_view(), name='verify-otp'),
]