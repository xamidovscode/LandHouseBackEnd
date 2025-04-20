from rest_framework.pagination import LimitOffsetPagination, CursorPagination
from rest_framework import serializers
import math
from rest_framework.response import Response


class CustomOffSetPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


def paginate(instances, serializer_class, request, **kwargs):
    paginator = CustomOffSetPagination()
    paginated_order = paginator.paginate_queryset(instances, request)

    serializer = serializer_class(paginated_order, many=True, **kwargs)

    return paginator.get_paginated_response(serializer.data)


class CustomOffSetDynamicPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100

    def __init__(self, page=None, limit=None):
        self.page = int(page) if page is not None else 1
        self.limit = int(limit) if limit is not None else self.default_limit

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        self.offset = (self.page - 1) * self.limit

        return queryset[self.offset:self.offset + self.limit]

    def get_limit(self, request):
        limit = super().get_limit(request)
        if limit is None:
            limit = self.limit
        return min(int(limit), self.max_limit)

    def get_paginated_response(self, data):
        total_elements = self.count
        total_pages = math.ceil(total_elements / self.limit)
        current_page = self.page

        return Response({
            'total': total_elements,
            'total_page': total_pages,
            'current_page': current_page,
            'results': data
        })


def paginate_dynamic(instances, serializer_class, request, page=1, limit=25, **kwargs):
    paginator = CustomOffSetDynamicPagination(page=page, limit=limit)

    paginator.count = instances.count()

    paginated_queryset = paginator.paginate_queryset(instances, request)

    serializer = serializer_class(paginated_queryset, many=True, **kwargs)

    return paginator.get_paginated_response(serializer.data)


class CustomCursorPagination(CursorPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = 'id'


def cursor_paginate(instances, serializer_class, request, **kwargs):
    paginator = CustomCursorPagination()
    paginated_order = paginator.paginate_queryset(instances, request)

    serializer = serializer_class(paginated_order, many=True, **kwargs)

    return paginator.get_paginated_response(serializer.data)


class PaginationResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(required=False, allow_null=True)
    previous = serializers.URLField(required=False, allow_null=True)
    results = serializers.ListSerializer(child=serializers.Serializer())

    def __init__(self, *args, **kwargs):
        self.child_serializer_class = kwargs.pop('child_serializer_class', serializers.Serializer)
        super().__init__(*args, **kwargs)
        self.fields['results'].child = self.child_serializer_class()


class PaginationDynamicResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    total_page = serializers.IntegerField()
    current_page = serializers.IntegerField()
    results = serializers.ListSerializer(child=serializers.Serializer())

    def __init__(self, *args, **kwargs):
        self.child_serializer_class = kwargs.pop('child_serializer_class', serializers.Serializer)
        super().__init__(*args, **kwargs)
        self.fields['results'].child = self.child_serializer_class()
