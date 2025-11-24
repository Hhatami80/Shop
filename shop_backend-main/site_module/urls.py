from django.urls import path
from . import views

urlpatterns = [
    # path('aboutus', views.AboutUsMainView.as_view(), name='about-us-main'),
    path("contact-info", views.ContactUsInfoView.as_view()),
    path("contact-messages", views.ContactUsMessageView.as_view()),
]
