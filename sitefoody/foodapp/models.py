from django.db import models
from django.urls import reverse
from django.conf import settings


class Dish(models.Model):
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    name = models.CharField(max_length=150, verbose_name='Название блюда')
    recipe = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField()
    special_menu = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['-time_create']


class Recipe(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название рецепта')
    content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тэг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Auth_User - Дефолтная табл
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']


class Blog(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название блога')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Auth_User - Дефолтная табл
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comment)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-time_create']


class Cook(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя повара')
    position = models.CharField(max_length=100, verbose_name='Должность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Повар'
        verbose_name_plural = 'Повары'
        ordering = ['id']


class Review(models.Model):
    content = models.TextField(blank=True)
    cook = models.ForeignKey(Cook, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['id']
