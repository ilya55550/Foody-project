from rest_framework import serializers, viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User, AnonymousUser

from foodapp.models import Dish, Category, Tag, Comment, Blog


class DishSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Dish
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    blog = serializers.SlugRelatedField(slug_field='name', queryset=Blog.objects.only('name'))

    class Meta:
        model = Comment
        fields = ('author', 'content', 'blog')

    # def create(self, validated_data):
    #     # override standard method to create cumster without pk in url
    #     # https://stackoverflow.com/questions/38745280/\
    #     # in-drfdjango-rest-framework-null-value-in-column-author-id-violates-not-nul
    #
    #     # validated_data['user_id'] = self.context['request'].user.id

    #     return super(CommentSerializer, self).create(validated_data)

    # def create(self, validated_data):
    #     if isinstance(self.context["request"].user, AnonymousUser):
    #         raise serializers.ValidationError('Вы не авторизованы', code=status.HTTP_401_UNAUTHORIZED)
    #
    #     return super(CommentSerializer, self).create(validated_data)


class ListBlogSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = ('name', 'author', 'image', 'content', 'time_create', 'category', 'tag')


class CreateUpdateDeleteBlogSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(slug_field='name', required=False, queryset=Category.objects.all())
    tag = serializers.SlugRelatedField(slug_field='name', required=False, queryset=Tag.objects.all())

    image = serializers.ImageField(required=False)

    class Meta:
        model = Blog
        fields = ('name', 'author', 'image', 'content', 'category', 'tag')
