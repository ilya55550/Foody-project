from django.urls import path
from rest_framework import routers

from .views_api import *

router = routers.SimpleRouter()
router.register('comments', CommentViewSet)

router1 = routers.SimpleRouter()
router1.register('blog', BlogViewSet, basename='blog')


urlpatterns = [
    path('dishs/', ListDish.as_view()),
    path('categories/', ListCategory.as_view()),
    path('tags/', ListTag.as_view()),
    # path('tags/', BlogViewSet.as_view()),

]

urlpatterns += router.urls
urlpatterns += router1.urls
