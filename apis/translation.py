from modeltranslation.translator import register, TranslationOptions
from apis import models


@register(models.Company)
class CompanyTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'address',
        'description',
    )


@register(models.Object)
class ObjectsTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'name',
        'description',
    )


@register(models.ObjectBlock)
class ObjectBlocksTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(models.New)
class NewsTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
    )


@register(models.Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
    )


@register(models.AboutCompany)
class AboutCompanyTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'obj1',
        'key1',
        'obj2',
        'key2',
        'obj3',
        'key3',
    )