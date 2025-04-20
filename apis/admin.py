from django.contrib import admin
from apis import models
from django.contrib.auth.models import Group, User

admin.site.site_title = "Land House Admin"
admin.site.site_header = "Land House"
admin.site.index_title = "Land House Admin"
admin.site.site_brand = "Land House"
admin.site.welcome_sign = "Land House"
admin.site.copyright = "Land House"

admin.site.unregister(Group)
# admin.site.unregister(User)

one = "1. Статистика компании"
two = "2. Объекты"
three = "3. Блоки"
four = "4. Заявка на общей информации"
five = "5. Заявка об объекте"
six = "6. Заявка на комнату"
seven = "7. Новости"
eight = "8. Баннер"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'objects_count', 'clients', 'years')
    list_display_links = ('name', 'objects_count', 'clients', 'years')


admin.site.register(models.Company, CompanyAdmin)


class ObjectPhotoInline(admin.StackedInline):
    model = models.ObjectPhoto
    extra = 1


class ObjectAdmin(admin.ModelAdmin):
    inlines = [ObjectPhotoInline]
    list_display = ('id', 'title', 'status', 'created_at')
    list_display_links = ('title', 'status', 'created_at')
    search_fields = ('title', 'name')
    list_filter = ['status']


admin.site.register(models.Object, ObjectAdmin)


class ObjectBlockRoomInline(admin.StackedInline):
    model = models.ObjectBlockRoom
    extra = 1


class ObjectBlockAdmin(admin.ModelAdmin):
    inlines = [ObjectBlockRoomInline]
    list_display = ('id', 'get_object_title', 'get_object_name', 'name', 'number')
    list_display_links = ('get_object_title', 'get_object_name', 'name', 'number')
    search_fields = ('object_pk__name', 'name',)
    list_filter = ['number']

    def get_object_title(self, obj):
        return obj.object_fk.title
    get_object_title.short_description = 'Объект Заголовок'

    def get_object_name(self, obj):
        return obj.object_fk.name
    get_object_name.short_description = 'Объект Название'


admin.site.register(models.ObjectBlock, ObjectBlockAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'status')
    list_display_links = ('full_name', 'phone',)
    list_editable = ['status']
    list_filter = ['status']


admin.site.register(models.Application, ApplicationAdmin)


class ApplicationObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_object_title', 'get_object_name', 'full_name', 'phone', 'status')
    list_display_links = ('get_object_title', 'get_object_name', 'full_name', 'phone',)
    list_editable = ['status']
    list_filter = ['status']

    def get_object_title(self, obj):
        return obj.object_fk.title
    get_object_title.short_description = 'Объект Заголовок'

    def get_object_name(self, obj):
        return obj.object_fk.name
    get_object_name.short_description = 'Объект Название'


admin.site.register(models.ApplicationObject, ApplicationObjectAdmin)


class ApplicationRoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_room_object_title',
        'get_room_object_name',
        'room_fk_block',
        'room_fk_count',
        'room_fk_floor',
        'room_fk_entrance',
        'full_name',
        'phone',
        'status'
    )
    list_display_links = (
        'get_room_object_title',
        'get_room_object_name',
        'full_name',
        'phone'
    )
    list_editable = ['status']
    list_filter = ['status']

    def get_room_object_title(self, obj):
        return obj.room_fk.object_fk.title
    get_room_object_title.short_description = 'Объект Заголовок'

    def get_room_object_name(self, obj):
        return obj.room_fk.object_fk.name
    get_room_object_name.short_description = 'Объект Название'

    def room_fk_block(self, obj):
        return obj.room_fk.block
    room_fk_block.short_description = 'Комната Блок'

    def room_fk_count(self, obj):
        return obj.room_fk.count
    room_fk_count.short_description = 'Комната Количество'

    def room_fk_floor(self, obj):
        return obj.room_fk.floor
    room_fk_floor.short_description = 'Комната Этаж'

    def room_fk_entrance(self, obj):
        return obj.room_fk.entrance
    room_fk_entrance.short_description = 'Комната Подъезд'


admin.site.register(models.ApplicationRoom, ApplicationRoomAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)


admin.site.register(models.New, NewsAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)

    fieldsets = (
        ('main', {'fields': ('url', 'youtube_url', 'image', )}),
        ('uz', {
            'fields': ('title_uz', 'description_uz')}),
        ('ru', {
            'fields': ('title_ru', 'description_ru')}),
    )


admin.site.register(models.Banner, BannerAdmin)


class AboutCompanyAdmin(admin.ModelAdmin):

    class ImagesInline(admin.TabularInline):
        model = models.AboutCompanyImages
        extra = 1

    inlines = [ImagesInline]

    list_display = ('id',)
    list_display_links = ('id',)
    fieldsets = (
        ('uz', {
            'fields': (
                'description_uz', 'obj1_uz', 'key1_uz', 'obj2_uz', 'key2_uz', 'obj3_uz', 'key3_uz'
            )}),
        ('ru', {
            'fields': (
                'description_ru', 'obj1_ru', 'key1_ru', 'obj2_ru', 'key2_ru', 'obj3_ru', 'key3_ru'
            )}),
    )

    def has_add_permission(self, request):
        return not models.AboutCompany.objects.first()


admin.site.register(models.AboutCompany, AboutCompanyAdmin)
