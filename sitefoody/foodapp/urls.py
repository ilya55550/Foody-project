from django.urls import path

from foodapp.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', about, name='about'),
]
