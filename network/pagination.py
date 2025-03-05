from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 10  # Default number of posts per page
    page_size_query_param = 'page_size'  # Allow changing page size via URL
    max_page_size = 50  # Maximum page size allowed
