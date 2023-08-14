from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    surname = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)


class MountainPass(models.Model):
    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey('Coordinates', on_delete=models.CASCADE)
    level = models.JSONField(default=dict, blank=True)
    images = models.ManyToManyField('Image')
    status = models.CharField(max_length=15, choices=(
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ))

    def create_pass(self, pass_data):
        pass_object = self.create(**pass_data)
        pass_object.status = "new"
        pass_object.save()
        return pass_object


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Image(models.Model):
    data = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
