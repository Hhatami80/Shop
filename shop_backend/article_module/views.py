from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

class ArticleView(APIView):

    def get(self, request: Request):
        articles = Article.objects.all()
        article_serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response({'articles': article_serializer.data}, status.HTTP_200_OK)


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
