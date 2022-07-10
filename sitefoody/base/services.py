from django.utils.text import slugify
from django.db.utils import IntegrityError
from rest_framework import serializers, status


def conversion_to_slug(from_conversion):
    result_conversion = slugify(from_conversion.translate(
        str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                      "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")))

    return result_conversion
