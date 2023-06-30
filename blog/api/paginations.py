from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        current_page = int(self.request.GET.get("page", 1))

        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": current_page,
                "first_page": 1,
                "last_page": self.page.paginator.num_pages,
                "data": data,
            }
        )