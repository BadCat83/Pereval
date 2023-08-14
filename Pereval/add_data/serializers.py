from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'surname', 'email', 'phone_number']


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class MountainPassSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordinatesSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = MountainPass
        fields = ['beauty_title', 'title', 'other_titles',
                  'connect', 'add_time', 'user', 'coords',
                  'level', 'images', 'status']
