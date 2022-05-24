from django.urls import path

from foodapp.views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
]
