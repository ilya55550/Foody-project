from django.contrib import admin
from .models import *


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'description', 'price', 'image', 'category', 'special_menu')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Dish, DishAdmin)
admin.site.register(Category)
