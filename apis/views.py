from django.db.models import Max
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from apis import models, serializers
from utils.languages import language
from utils.pagination import PaginationDynamicResponseSerializer, paginate_dynamic
from apis.exceptions import error_exception, ErrorCodes
from rest_framework import exceptions, generics
from rest_framework.response import Response
from utils.responses import success, response_schema


class BaseAPIView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        lang = request.headers.get('lang', 'uz')
        language(lang)

        return request


class CompanyAPIView(BaseAPIView):
    @extend_schema(
        summary="Company statistics",
        request=None,
        responses=serializers.CompanySerializer,
    )
    def get(self, request):
        company = models.Company.objects.first()
        ser = serializers.CompanySerializer(company)
        return Response(ser.data, 200)


class ObjectsAPIView(BaseAPIView):
    @extend_schema(
        summary="Objects",
        request=None,
        responses=PaginationDynamicResponseSerializer(child_serializer_class=serializers.ObjectsSerializer),
        parameters=[
            OpenApiParameter(name='page', required=True, type=OpenApiTypes.INT),
            OpenApiParameter(name='limit', required=True, type=OpenApiTypes.INT),
        ]
    )

    def get(self, request):
        page = request.query_params.get('page')
        limit = request.query_params.get('limit')

        objects = models.Object.objects.all().prefetch_related('photos').order_by('-created_at')

        return paginate_dynamic(objects, serializers.ObjectsSerializer, request, page, limit)


class ObjectAPIView(BaseAPIView):
    @extend_schema(
        summary="Object",
        request=None,
        responses=serializers.ObjectDetailSerializer,
        parameters=[
            OpenApiParameter(name="pk", description="Object ID", type=OpenApiTypes.INT, required=True),
        ]
    )

    def get(self, request):
        pk = request.query_params.get('pk')

        try:
            obj = models.Object.objects.prefetch_related('photos', 'blocks').get(id=pk)
        except models.Object.DoesNotExist:
            raise error_exception(
                exceptions.NotFound,
                ErrorCodes.OBJECT_NOT_FOUND
            )

        ser = serializers.ObjectDetailSerializer(obj)

        return Response(ser.data, 200)


class ObjectMainAPIView(BaseAPIView):
    @extend_schema(
        summary="Object main",
        request=None,
        responses=serializers.ObjectMainSerializer,
    )
    def get(self, request):

        obj = models.Object.objects.filter(main=True).last()
        if not obj:
            obj = models.Object.objects.all().last()

        ser = serializers.ObjectMainSerializer(obj)

        return Response(ser.data, 200)


class ObjectRoomAPIView(BaseAPIView):
    @extend_schema(
        summary="Room",
        request=None,
        responses=serializers.ObjectBlockRoomDetailSerializer,
        parameters=[
            OpenApiParameter(name="pk", description="Room ID", type=OpenApiTypes.INT, required=True)
        ]
    )
    def get(self, request):
        pk = request.query_params.get('pk')

        try:
            room = models.ObjectBlockRoom.objects.get(id=pk)
        except models.ObjectBlockRoom.DoesNotExist:
            raise error_exception(
                exceptions.NotFound,
                ErrorCodes.ROOM_NOT_FOUND
            )
        ser = serializers.ObjectBlockRoomDetailSerializer(room)
        return Response(ser.data, 200)


class ObjectRoomFilterAPIView(BaseAPIView):
    @extend_schema(
        summary="Room Filter",
        request=None,
        responses=serializers.ObjectBlockRoomsSerializer,
        parameters=[
            OpenApiParameter(name="object", description="Object ID", type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name="block", description="Block ID", type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name="entrance", type=OpenApiTypes.INT, required=False),
            OpenApiParameter(name="floor", type=OpenApiTypes.INT, required=False),
        ]
    )
    def get(self, request):
        object = request.query_params.get('object')
        block = request.query_params.get('block')
        entrance = request.query_params.get('entrance')
        floor = request.query_params.get('floor')

        filter_criteria = {}

        if object:
            filter_criteria['block_fk__object_fk'] = object

        if block:
            filter_criteria['block_fk'] = block

        if entrance:
            filter_criteria['entrance'] = entrance

        if floor:
            filter_criteria['floor'] = floor

        rooms = models.ObjectBlockRoom.objects.filter(**filter_criteria)

        ser = serializers.ObjectBlockRoomsSerializer(rooms, many=True)
        return Response(ser.data, 200)


class ObjectRoomFilterChoicesAPIView(BaseAPIView):
    @extend_schema(
        summary="Room Filter Choices",
        request=None,
        responses=None,
        parameters=[
            OpenApiParameter(name="pk", description="Object ID", type=OpenApiTypes.INT, required=True)
        ]
    )
    def get(self, request):
        pk = request.query_params.get('pk')

        obj_blocks = models.ObjectBlock.objects.filter(object_fk=pk).all()

        block_data = []
        for block in obj_blocks:
            max_entrance = block.rooms.aggregate(Max('entrance'))['entrance__max']
            max_floor = block.rooms.aggregate(Max('floor'))['floor__max']

            serialized_block = serializers.ObjectBlocksChoicesSerializer(block).data

            serialized_block['max_entrance'] = max_entrance
            serialized_block['max_floor'] = max_floor

            block_data.append(serialized_block)

        return Response(block_data, 200)


class ApplicationsAPIView(APIView):
    @extend_schema(
        summary="Create Application",
        request=serializers.ApplicationCreateSerializer,
        responses=response_schema
    )
    def post(self, request):
        ser = serializers.ApplicationCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return success


class NewsAPIView(BaseAPIView):
    @extend_schema(
        summary="News",
        request=None,
        responses=PaginationDynamicResponseSerializer(child_serializer_class=serializers.NewsSerializer),
        parameters=[
            OpenApiParameter(name='page', required=True, type=OpenApiTypes.INT),
            OpenApiParameter(name='limit', required=True, type=OpenApiTypes.INT),
        ]
    )
    def get(self, request):
        page = request.query_params.get('page')
        limit = request.query_params.get('limit')

        news = models.New.objects.all().order_by('-id')

        return paginate_dynamic(news, serializers.NewsSerializer, request, page, limit)


class NewAPIView(BaseAPIView):
    @extend_schema(
        summary="New",
        request=None,
        responses=serializers.NewDetailSerializer,
        parameters=[
            OpenApiParameter(name="pk", description="New ID", type=OpenApiTypes.INT, required=True)
        ]
    )
    def get(self, request):
        pk = request.query_params.get('pk')

        try:
            new = models.New.objects.get(id=pk)
        except models.New.DoesNotExist:
            raise error_exception(
                exceptions.NotFound,
                ErrorCodes.NEW_NOT_FOUND
            )

        ser = serializers.NewDetailSerializer(new)

        return Response(ser.data, 200)



class BannerListAPIView(generics.ListAPIView):
    queryset = models.Banner.objects.all()
    serializer_class = serializers.BannerListSerializer
    pagination_class = None


class AboutCompanyListAPIView(generics.RetrieveAPIView):
    queryset = models.AboutCompany.objects.all()
    serializer_class = serializers.AboutCompanySerializer
    pagination_class = None


    def get_object(self):
        return models.AboutCompany.objects.first()