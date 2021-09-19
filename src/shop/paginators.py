from rest_framework.pagination import LimitOffsetPagination


class ProductsPaginator(LimitOffsetPagination):
    page_size = 100
    page_size_query_param = 'page_size'
