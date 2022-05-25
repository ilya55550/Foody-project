from django.urls import path

from foodapp.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('blogs/', BlogsPage.as_view(), name='blogs'),
]
