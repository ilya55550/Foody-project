from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
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


class CategoryBlogPage(ListView):
    model = Blog
    template_name = 'foodapp/category_blogs.html'
    context_object_name = 'blogs'
    paginate_by = 4

    def get_queryset(self):
        return Blog.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        return context | {'category_slug': category_slug}


class DetailBlogPage(DetailView):
    model = Blog
    template_name = 'foodapp/detail_blog.html'
    slug_url_kwarg = 'detail_slug'
    context_object_name = 'blog'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_blogs = CategoryBlog.objects.all()[:5]
        return context | {'category_blogs': category_blogs}
