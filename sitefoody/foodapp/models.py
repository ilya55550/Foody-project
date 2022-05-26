from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=40, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="photo_user/%Y/%m/%d/")

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['id']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Dish(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название блюда')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    recipe = models.TextField()
    description = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="image/%Y/%m/%d/")
    special_menu = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['-time_create']


class Category(models.Model):
    """Категории блюд"""
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Тэг')

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.name[0] != '#':
    #         self.name = '#' + self.name
    #     super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['id']


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    blog = models.OneToOneField('Blog', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']


class Blog(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название блога')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="image/%Y/%m/%d/")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('CategoryBlog')
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_blog', kwargs={'detail_slug': self.slug})

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-time_create']


class Cook(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя повара')
    position = models.CharField(max_length=100, verbose_name='Должность')
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/")

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


class CategoryBlog(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_blog', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блогов'
        ordering = ['id']
