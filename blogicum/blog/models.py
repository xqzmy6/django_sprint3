from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                       'чтобы скрыть публикацию.')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    slug = models.SlugField(max_length=64, unique=True,
                            verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, '
                            'цифры, дефис и подчёркивание.')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название места')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                       'чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, verbose_name='Автор публикации')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                       'чтобы скрыть публикацию.')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — можно делать '
                                    'отложенные публикации.')
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='post_set')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title