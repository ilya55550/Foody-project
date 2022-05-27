from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *


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
    allow_empty = False

    def get_queryset(self):
        return Blog.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_model = CategoryBlog.objects.get(slug=self.kwargs['category_slug'])
        category = category_model.name
        return context | {'category': category}


class TagBlogPage(ListView):
    model = Blog
    template_name = 'foodapp/tag_blogs.html'
    context_object_name = 'blogs'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Blog.objects.filter(tag__slug=self.kwargs['tag_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['tag_slug']
        return context | {'tag_slug': tag_slug}


class DetailBlogPage(FormMixin, DetailView):
    model = Blog
    slug_url_kwarg = 'detail_slug'
    template_name = 'foodapp/detail_blog.html'
    context_object_name = 'blog'
    form_class = CreateCommentForm

    def get_success_url(self):
        return reverse('detail_blog', kwargs={'detail_slug': self.get_object().slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_blogs'] = CategoryBlog.objects.all()[:5]
        context['form'] = CreateCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.blog = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
