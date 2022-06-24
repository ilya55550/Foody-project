from django.contrib import admin
from django.urls import path, include
from sitefoody import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('foodapp.urls')),
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/', include('foodapp_api.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)