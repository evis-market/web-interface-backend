from rest_framework.pagination import LimitOffsetPagination


class ProductsPaginator(LimitOffsetPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    default_limit = 50
