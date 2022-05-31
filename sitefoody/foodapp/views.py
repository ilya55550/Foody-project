import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormMixin, FormView
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from django.core.mail import send_mail
from .utils import *
from decouple import config


class HomePage(View):
    def get(self, request):
        special_menu = Dish.objects.filter(special_menu=True)[:5]
        dishs = Dish.objects.filter(special_menu=False)[:8]
        reviews = Review.objects.all().select_related('cook')
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

    def get_queryset(self):
        return Blog.objects.filter(slug=self.kwargs['detail_slug']).select_related('author__profile')

    def get_success_url(self):
        return reverse('detail_blog', kwargs={'detail_slug': self.get_object().slug})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_blogs'] = CategoryBlog.objects.all()[:5]
        context['comments'] = Comment.objects.filter(blog__slug=self.kwargs['detail_slug']).defer(
            "blog").select_related('author__profile')
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


class RecipesPage(ListView):
    model = Dish
    template_name = 'foodapp/recipes.html'
    context_object_name = 'dishs'


class AboutPage(ListView):
    model = Cook
    template_name = 'foodapp/about.html'
    context_object_name = 'cooks'


class ContactPage(FormView):
    form_class = ContactForm
    template_name = 'foodapp/contact.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        name_country = country_definition(form.cleaned_data['phone'].country_code)
        message = form.cleaned_data['message'] + \
                  f"\n\nДанные отправителя:" \
                  f"\nТелефон: {form.cleaned_data['phone']}, Страна: {name_country}" \
                  f"\nEmail: {form.cleaned_data['email']}"
        send_mail('Contact', message, config('EMAIL_HOST_USER'), [config('EMAIL_RECEIVES_MESSAGES')],
                  fail_silently=False)
        return super(ContactPage, self).form_valid(form)
