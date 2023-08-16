from rest_framework.response import Response

from .models import *
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    @staticmethod
    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fam', 'name', 'otc', 'email', 'phone']


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Image
        fields = ['image', 'title']


class MountainPassAddSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordinatesSerializer()

    class Meta:
        model = MountainPass
        fields = ['beauty_title', 'title', 'other_titles', 'connect',
                  'add_time', 'user', 'coords', 'level']

    # Необходимый метод для создания объектов User и Coordinates
    def create(self, validated_data):
        user_ser = (UserSerializer(data=validated_data['user']))
        if not user_ser.is_valid():
            return Response({'status': 400, 'message': 'Invalid user data', 'id': None})
        validated_data['user'] = user_ser.save()

        coord_ser = CoordinatesSerializer(data=validated_data['coords'])
        if not coord_ser.is_valid():
            return Response({'status': 400, 'message': 'Invalid coordinate data', 'id': None})
        validated_data['coords'] = coord_ser.save()

        validated_data['status'] = 'new'

        instance = MountainPass.objects.create(**validated_data)

        return instance


class MountainPassEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MountainPass
        depth = 1
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'level', 'images']
