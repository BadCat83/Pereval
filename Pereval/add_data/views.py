from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="Get the list of users")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new user")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a user by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a user by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a user by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CoordinatesViewSet(viewsets.ModelViewSet):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinatesSerializer

    @swagger_auto_schema(operation_description="Get the list of coordinates")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new coordinate")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a coordinate by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a coordinate by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a coordinate by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @swagger_auto_schema(operation_description="Get the list of images")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new image")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve an image by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an image by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete an image by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PassViewSet(viewsets.ModelViewSet):
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassSerializer

    @swagger_auto_schema(operation_description="Get the list of passes")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new pass")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a pass by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a pass by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a pass by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@swagger_auto_schema(method='POST', operation_description='Submit data')
@api_view(['POST'])
def submitData(request):
    data = request.data
    # Проверка на наличие требуемых полей
    required_fields = ['beauty_title', 'title', 'other_titles', 'connect',
                       'user', 'coords', 'level',  'images']
    if not all(field in data for field in required_fields):
        return Response({'status': 400, 'message': 'There are no all required  field!', 'id': None})
    try:
        level_data = data.get('level')

        # Проверка наличия обязательных параметров в поле level
        required_level_fields = ['winter', 'summer', 'autumn', 'spring']
        if not all(field in level_data for field in required_level_fields):
            return Response({'status': 400, 'message': 'Missing required fields in "level!"', 'id': None})

        # Проверка на корректность данных
        if not all(isinstance(level_data[field], str) for field in required_level_fields):
            return Response({'status': 400, 'message': 'Invalid format in "level"', 'id': None})
        # Внесение данных по объекту
        pass_data = {
            'beauty_title': data['beauty_title'],
            'title': data['title'],
            'other_titles': data['other_titles'],
            'connect': data['connect'],
            'add_time': datetime.now(),
            'user': data['user'],
            'coords': data['coords'],
            'level': level_data,
            'status': 'new'
        }
        # Сохраняем объект
        pass_serializer = MountainPassSerializer(data=pass_data)
        if not pass_serializer.is_valid(raise_exception=True):
            return Response({'status': 400, 'message': 'Invalid pass data', 'id': None})
        pass_object = pass_serializer.save()
        # Работаем с фото
        images_data = data.get('images')
        if images_data is None:
            return Response({'status': 400, 'message': 'Field "images" is required', 'id': None})
        # Проверка наличия обязательных подполей в поле images
        required_image_fields = ['image', 'title']
        img = []
        for image_data in images_data:
            if not all(field in image_data for field in required_image_fields):
                return Response({'status': 400, 'message': 'Missing required fields in "images"', 'id': None})

            # Дополнительные проверки формата или значений подполей в поле images
            if not isinstance(image_data['image'], str) or not isinstance(image_data['title'], str):
                return Response({'status': 400, 'message': 'Invalid format in "images"', 'id': None})
            # Создаем объекты и готовим список для привязки к основному объекту
            image_serializer = ImageSerializer(data=image_data)
            if not image_serializer.is_valid():
                return Response({'status': 400, 'message': 'Invalid image data', 'id': None})
            img.append(image_serializer.save())
        # Привязываем фото к объекту
        pass_object.images.set(img)

        return Response({'status': 200, 'message': 'Data submitted successfully', 'id': pass_object.id})
    except (ValidationError, Exception) as e:
        return Response({'status': 500, 'message': str(e), 'id': None})
