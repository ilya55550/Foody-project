from django.shortcuts import render
from django.views import View
from .models import *


class HomePage(View):
    def get(self, request):
        special_menu = Dish.objects.filter(special_menu=True)[:2]
        dishs = Dish.objects.all()[:8]
        reviews = Review.objects.all()
        context = {
            'special_menu': special_menu,
            'dishs': dishs,
            'reviews': reviews,
        }
        return render(request, 'foodapp/index.html', context=context)


def about(request):
    return render(request, 'foodapp/index.html')
