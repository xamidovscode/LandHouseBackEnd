from rest_framework import serializers
from apis import models


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = [
            'name',
            'phone',
            'email',
            'you_tube',
            'instagram',
            'telegram',
            'facebook',
            'objects_count',
            'clients',
            'years',
            'address',
            'longitude',
            'latitude',
            'description',
        ]


class ObjectPhotosSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = models.ObjectPhoto
        fields = [
            'id',
            'photo'
        ]

    def get_photo(self, obj) -> str:
        if obj.photo:
            return obj.photo.url
        return None


class ObjectsSerializer(serializers.ModelSerializer):
    photos = ObjectPhotosSerializer(many=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.Object
        fields = [
            'id',
            'title',
            'name',
            'description',
            'status',
            'created_at',
            'photos',
            'video',
            'longitude',
            'latitude',
        ]

    def get_description(self, obj) -> str:
        max_length = 20
        description = obj.description
        if len(description) > max_length:
            return description[:max_length] + '...'
        return description


class ObjectBlockRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectBlockRoom
        fields = [
            'id',
            'photo',
            'total_area',
            'count',
        ]

    def get_photo(self, obj) -> str:
        if obj.photo:
            return obj.photo.url
        return None


class ObjectBlocksSerializer(serializers.ModelSerializer):
    rooms = ObjectBlockRoomsSerializer(many=True)

    class Meta:
        model = models.ObjectBlock
        fields = [
            'id',
            'name',
            'number',
            'rooms',
        ]

    def get_rooms(self, obj):
        rooms = obj.rooms.all().order_by('count')
        return ObjectBlockRoomsSerializer(rooms, many=True).data


class ObjectBlocksChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectBlock
        fields = [
            'id',
            'name',
            'number',
        ]


class ObjectDetailSerializer(serializers.ModelSerializer):
    photos = ObjectPhotosSerializer(many=True)
    blocks = ObjectBlocksSerializer(many=True)

    class Meta:
        model = models.Object
        fields = [
            'id',
            'title',
            'name',
            'description',
            'status',
            'created_at',
            'photos',
            'blocks',
            'video',
            'longitude',
            'latitude',
        ]


class ObjectMainSerializer(serializers.ModelSerializer):
    photos = ObjectPhotosSerializer(many=True)

    class Meta:
        model = models.Object
        fields = [
            'id',
            'title',
            'name',
            'description',
            'status',
            'created_at',
            'photos',
            'video',
            'longitude',
            'latitude',
        ]


class ObjectBlockRoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ObjectBlockRoom
        fields = [
            'id',
            'photo',
            'total_area',
            'count',
            'floor',
            'entrance',
            'price',
        ]


class ApplicationCreateSerializer(serializers.Serializer):
    object_id = serializers.IntegerField(required=False, allow_null=True)
    room_id = serializers.IntegerField(required=False, allow_null=True)
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)

    def validate(self, attrs):
        object_id = attrs.get('object_id')
        room_id = attrs.get('room_id')

        if object_id and room_id:
            raise serializers.ValidationError("You cannot provide both object_id and room_id.")

        if not object_id and not room_id:
            return attrs

        if object_id:
            if not models.Object.objects.filter(id=object_id).exists():
                raise serializers.ValidationError("Invalid object_id provided.")

        if room_id:
            if not models.ObjectRoom.objects.filter(id=room_id).exists():
                raise serializers.ValidationError("Invalid room_id provided.")

        return attrs

    def create(self, validated_data):
        object_id = validated_data.get('object_id')
        room_id = validated_data.get('room_id')
        full_name = validated_data.get('full_name')
        phone = validated_data.get('phone')

        if room_id:
            room = models.ObjectRoom.objects.get(id=room_id)
            return models.ApplicationRoom.objects.create(
                room_fk=room,
                full_name=full_name,
                phone=phone,
            )
        elif object_id:
            obj = models.Object.objects.get(id=object_id)
            return models.ApplicationObject.objects.create(
                object_fk=obj,
                full_name=full_name,
                phone=phone,
            )
        else:
            return models.Application.objects.create(
                full_name=full_name,
                phone=phone,
            )


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.New
        fields = [
            'id',
            'title',
            'description',
            'photo',
        ]

    # def get_description(self, obj) -> str:
    #     max_length = 100
    #     description = obj.description
    #     if len(description) > max_length:
    #         return description[:max_length] + '...'
    #     return description


class NewDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.New
        fields = [
            'id',
            'title',
            'description',
            'photo',
        ]
