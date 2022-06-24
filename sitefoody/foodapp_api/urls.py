from django.urls import path
from rest_framework import routers

from .views_api import *

router_comment = routers.SimpleRouter()
router_comment.register('comments', CommentViewSet)

router_blog = routers.SimpleRouter()
router_blog.register('blog', BlogViewSet, basename='blog')

list_routers = [router_comment, router_blog]

urlpatterns = [
    path('dishs/', ListDish.as_view()),
    path('categories/', ListCategory.as_view()),
    path('tags/', ListTag.as_view()),

]

for router in list_routers:
    urlpatterns += router.urls
