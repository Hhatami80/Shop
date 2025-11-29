from django.urls import path

from comments.views import ArticleCommentView

urlpatterns = [
    path('articles/<int:pk>/comments', ArticleCommentView.as_view()),

]