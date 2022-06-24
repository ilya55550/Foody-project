from rest_framework import viewsets, generics, viewsets, mixins, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from foodapp.models import Dish, Category, Tag, Comment, Blog
from .permissions import IsOwnerOrReadOnly
from .serializers import DishSerializer, CategorySerializer, TagSerializer, CommentSerializer, ListBlogSerializer, \
    CreateUpdateDeleteBlogSerializer


class ListDish(generics.ListAPIView):
    serializer_class = DishSerializer
    queryset = Dish.objects.all().select_related('category')


class ListCategory(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ListTag(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


# viewsets.ModelViewSet
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # добавляем автора комментария в ответ пользователю
        response_to_user = serializer.data
        response_to_user['author'] = str(serializer.validated_data['author'])

        return Response(response_to_user, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     """Сохранение комментария"""
    #     serializer.save(author=self.request.user)


class BlogViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Blog.objects.all()
    serializer_class = CreateUpdateDeleteBlogSerializer
    permission_classes_by_action = {'create': [IsOwnerOrReadOnly, IsAuthenticated],
                                    'update': [IsOwnerOrReadOnly, IsAuthenticated],
                                    'partial_update': [IsOwnerOrReadOnly, IsAuthenticated],
                                    'destroy': [IsOwnerOrReadOnly, IsAuthenticated],
                                    'retrieve': [IsOwnerOrReadOnly, IsAuthenticated],
                                    'list': [AllowAny]}

    def list(self, request, *args, **kwargs):
        queryset = Blog.objects.all()

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = ListBlogSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


