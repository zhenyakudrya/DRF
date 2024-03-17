from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 30


class CoursePaginator(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 30
