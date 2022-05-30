from django.urls import path

from foodapp.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('blogs/', BlogsPage.as_view(), name='blogs'),
    path('blogs/category/<slug:category_slug>/', CategoryBlogPage.as_view(), name='category_blog'),
    path('blogs/tag/<slug:tag_slug>/', TagBlogPage.as_view(), name='tag_blog'),
    path('blogs/<slug:detail_slug>/', DetailBlogPage.as_view(), name='detail_blog'),
    path('recipes/', RecipesPage.as_view(), name='recipes'),
    path('about/', AboutPage.as_view(), name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
]
