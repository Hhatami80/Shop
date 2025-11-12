from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 5  # default items per page
    page_size_query_param = 'per_page'  # allows ?page_size=20
    max_page_size = 100  # safety limit
