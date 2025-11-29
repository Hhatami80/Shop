from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions, generics

from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.shortcuts import get_object_or_404

from account_module.permissions import IsAdmin
from .models import Comment
from .serializers import CommentSerializer
from article_module.models import Article


class ArticleCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Article),
            object_id=kwargs.get('pk'),
            content=serializer.validated_data["content"],
            parent=serializer.validated_data.get("parent")
        )
        return Response(CommentSerializer(comment))

    def get_queryset(self):
        queryset = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Article))
        if self.request.user.role != 'admin':
            queryset = queryset.filter(is_approved=True)
        return queryset
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny]
        else:
            return [IsAdmin()]