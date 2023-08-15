from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    fam = models.CharField(max_length=100, verbose_name='Фамилия')
    otc = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)


class MountainPass(models.Model):
    beauty_title = models.CharField(max_length=100, verbose_name='Тип')
    title = models.CharField(max_length=100, verbose_name='Название')
    other_titles = models.CharField(max_length=100, verbose_name="Другие названия")
    connect = models.TextField(blank=True, verbose_name='Описание')
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey('Coordinates', on_delete=models.CASCADE)
    level = models.JSONField(default=dict, blank=True, verbose_name='Сложность прохождения')
    images = models.ManyToManyField('Image', blank=True, verbose_name='Фотографии',)
    status = models.CharField(max_length=15, choices=(
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ), verbose_name='Статус модерирования')


class Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота над уровнем моря')


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100, verbose_name='Описание', blank=True)
