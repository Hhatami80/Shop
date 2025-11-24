from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from .serializers import ContactUsInfoSerializer, ContactUsMessageSerializer
from .models import ContactUsInfo


# Create your views here.
class ContactUsInfoView(RetrieveUpdateAPIView):
    serializer_class = ContactUsInfoSerializer

    def get_object(self):
        return ContactUsInfo.objects.first()

class ContactUsMessageView(CreateAPIView):
    serializer_class = ContactUsMessageSerializer