from django.contrib import admin
from .models import *


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'description', 'price', 'image', 'category', 'special_menu')
    prepopulated_fields = {'slug': ('name',)}


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(Cook)
admin.site.register(Review)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Dish, DishAdmin)
admin.site.register(Category)
