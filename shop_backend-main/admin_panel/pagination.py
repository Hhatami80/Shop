from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil

class AdminCommentPaginator(PageNumberPagination):
    page_size = 50
    page_query_param = "page"
    page_size_query_param = "per_page"
    
    def get_paginated_response(self, data):
        # total_pages = ceil(self.page.paginator.count / self.page_size)

        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "results": data
        })