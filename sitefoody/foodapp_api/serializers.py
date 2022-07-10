from django.db import IntegrityError
from rest_framework import serializers, viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User, AnonymousUser
from django.utils.text import slugify

from foodapp.models import Dish, Category, Tag, Comment, Blog, CategoryBlog
from base.services import conversion_to_slug


class DishSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Dish
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryBlog
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
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = CategoryBlogSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ('name', 'author', 'image', 'content', 'time_create', 'category', 'tag')


class CreateUpdateDeleteBlogSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # category = serializers.SlugRelatedField(slug_field='name', required=False, queryset=CategoryBlog.objects.all())
    # tag = serializers.SlugRelatedField(slug_field='name', required=False, queryset=Tag.objects.all())

    category = CategoryBlogSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)

    image = serializers.ImageField(required=False)

    class Meta:
        model = Blog
        fields = ('name', 'author', 'image', 'content', 'category', 'tag')

    def create(self, validated_data):
        print(validated_data)

        # categories = validated_data.pop('category')
        # tags = validated_data.pop('tag')

        validated_data['slug'] = conversion_to_slug(validated_data['name'])
        print(f'validated_data: {validated_data}')

        try:
            blog = Blog.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Сгенерированный slug совпадает с существующим',
                                              code=status.HTTP_400_BAD_REQUEST)
        print('create-------')
        # for category in categories:
        #     # d = dict(person)
        #     obj, created = CategoryBlog.objects.get_or_create(name=category)
        # print('---------------')
        # print(obj)
        # print(created)
        # print('---------------')
        return blog
    # return super(CreateUpdateDeleteBlogSerializer, self).create(validated_data)
