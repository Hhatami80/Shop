from rest_framework.pagination import PageNumberPagination

class AdminCommentPaginator(PageNumberPagination):
    page_size = 50
    page_query_param = "page"
    page_size_query_param = "per_page"
