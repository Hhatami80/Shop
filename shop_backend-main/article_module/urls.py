from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleView.as_view(), name='article'),
    path('articles-edit/<int:pk>/', views.ArticleDetail.as_view(), name='article'),
    path("articles/upload-image/", views.ArticleImageUpload.as_view(), name="upload-article-image"),
]