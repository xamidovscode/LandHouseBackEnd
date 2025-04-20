from django.utils import translation


def language(lang):
    if lang == 'ru':
        translation.activate('ru')
    else:
        translation.activate('uz')
