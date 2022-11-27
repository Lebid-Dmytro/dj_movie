from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    '''Категорії'''
    name = models.CharField('Категорії', max_length=150)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

class Actor(models.Model):
    '''Актори та режисери'''
    name = models.CharField("Ім'я", max_length=100)
    age = models.PositiveSmallIntegerField('Вік', default=0)
    description = models.TextField('Опис')
    image = models.ImageField('Фото', upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = 'Актори та режисери'
        verbose_name_plural = 'Актори та режисери'


class Genre(models.Model):
    '''Жанри'''
    name = models.CharField("Ім'я", max_length=100)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Movie(models.Model):
    '''Фільм'''
    title = models.CharField('Назва', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Опис')
    poster = models.ImageField('Постер', upload_to='movie/')
    year = models.PositiveSmallIntegerField("Дата прем'єри", default=2022)
    country = models.CharField('Країна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Режисер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актори', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанри')
    worlds_premiere = models.DateField("Прем'єра в світі", default=date.today)
    budget = models.PositiveSmallIntegerField('Бюджет', default=0, help_text='ціна в $')
    fess_in_usa = models.PositiveSmallIntegerField(
        'Збори в США', default=0, help_text='ціна в $'
    )
    fess_in_world = models.PositiveSmallIntegerField(
        'Збори в світі', default=0, help_text='ціна в $'
    )
    category = models.ForeignKey(
        Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField('Чорновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'


class MovieShots(models.Model):
    '''Кадри з фільму'''
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Опис')
    image = models.ImageField('Фото', upload_to='movie_shorts/')
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр з фільму'
        verbose_name_plural = 'Кадри з фільму'


class RettingStar(models.Model):
    '''Зірки рейтингу'''
    value = models.PositiveSmallIntegerField('Значення', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'
        ordering = ['-value']


class Rating(models.Model):
    '''Рейтинг'''
    ip = models.CharField('IP адреса', max_length=20)
    star = models.ForeignKey(RettingStar, on_delete=models.CASCADE, verbose_name='зірка')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фільм')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    '''Відгуки'''
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=100)
    test = models.TextField('Повідомлення', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Батьківська', on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

