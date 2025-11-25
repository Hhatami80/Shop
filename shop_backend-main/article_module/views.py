from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import ListCreateAPIView
from account_module.permissions import IsAdmin



# Create your views here.
class ArticleView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    parser_classes =  [JSONParser, MultiPartParser, FormParser]
    queryset = Article.objects.all()


class ArticleDetail(APIView):
    def get(self, request: Request, article_id):
        article = Article.objects.get(pk=article_id)
        article_serializer = ArticleSerializer(article, context={'request': request})
        return Response({'articles': article_serializer.data}, status.HTTP_200_OK)
#
#     def post(self, request: Request):
#         article_serializer = ArticleSerializer(data=request.data)
#         if article_serializer.is_valid():
#             article_serializer.save()
#             return Response({'data': 'مقاله با موفقیت اضافه شد'}, status.HTTP_200_OK)
#         return Response({'errors': article_serializer.data}, status.HTTP_400_BAD_REQUEST)
#
#
# class UpdateDeleteArticleView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request: Request, article_id):
#         articles = Article.objects.get(pk=article_id)
#         article_serializer = ArticleSerializer(articles, context={'request': request})
#         return Response({'articles': article_serializer.data}, status.HTTP_200_OK)
#
#     def put(self, request: Request, article_id):
#         articles = Article.objects.get(pk=article_id)
#         article_serializer = ArticleSerializer(articles, data=request.data, partial=True)
#         if article_serializer.is_valid():
#             article_serializer.save()
#             return Response({'data': 'مقاله با موفقیت آپدیت شد'}, status.HTTP_200_OK)
#
#         return Response({'errors': article_serializer.errors}, status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request: Request, article_id):
#         articles = Article.objects.get(pk=article_id)
#         articles.delete()
#         return Response({'data': 'مقاله با موفقیت حذف شد'}, status.HTTP_200_OK)

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