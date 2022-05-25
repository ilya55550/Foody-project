
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import *


class HomePage(View):
    def get(self, request):
        special_menu = Dish.objects.filter(special_menu=True)[:5]
        dishs = Dish.objects.filter(special_menu=False)[:8]
        reviews = Review.objects.all()
        blogs = Blog.objects.all()[:2]
        categories = Category.objects.all()[:4]
        context = {
            'special_menu': special_menu,
            'dishs': dishs,
            'reviews': reviews,
            'blogs': blogs,
            'categories': categories
        }
        return render(request, 'foodapp/index.html', context=context)


class BlogsPage(ListView):
    model = Blog
    template_name = 'foodapp/blogs.html'
    context_object_name = 'blogs'
    paginate_by = 4


