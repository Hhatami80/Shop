from django.shortcuts import render
from django.core.files.storage import default_storage

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from .models import Article
from .serializers import ArticleSerializer
from account_module.permissions import IsAdmin



# Create your views here.
class ArticleView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    parser_classes =  [JSONParser, MultiPartParser, FormParser]
    
    def get_queryset(self):
        if self.request.user.role == "admin":
            return Article.objects.all()
        return Article.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdmin()]


class ArticleDetail(RetrieveDestroyAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        if self.request.user.role != "admin":
            return Article.objects.filter(is_published=True)
        return Article.objects.all()
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
# class ArticleDetail(APIView):
#     def get(self, request: Request, article_id):
#         article = Article.objects.get(pk=article_id)
#         article_serializer = ArticleSerializer(article, context={'request': request})
#         return Response({'articles': article_serializer.data}, status.HTTP_200_OK)


class ArticleImageUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request: Request):
        image = request.FILES.get("file")
        
        if not image:
            return Response({
                "error": "تصویری ارسال نشده است."
            }, status=404)
        path = default_storage.save(f"article_images/{image.name}", image)
        url = default_storage.url(path)
        abs_url = request.build_absolute_uri(url)
        return Response({
            "url": abs_url
        }, status.HTTP_200_OK)