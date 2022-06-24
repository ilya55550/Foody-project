from django.urls import path, include

from foodapp.views import *

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth_token/', include('djoser.urls.authtoken')),
]
