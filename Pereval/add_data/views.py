from rest_framework import viewsets, mixins
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics


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
    serializer_class = MountainPassAddSerializer

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


class MountainPassAddView(generics.CreateAPIView):
    """Добавление объектов"""
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassAddSerializer

    def post(self, request):

        data = request.data
        pass_serializer = MountainPassAddSerializer(data=data)
        if pass_serializer.is_valid(raise_exception=True):
            pass_object = pass_serializer.save()
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


class MountainPassEditView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Редактирование объектов"""
    queryset = MountainPass.objects.all()
    serializer_class = MountainPassEditSerializer

    def update(self, request, *args, **kwargs):

        pk = kwargs.get("pk", None)

        try:
            instance = MountainPass.objects.get(pk=pk)
        except Exception as e:
            return Response({"Error": f"Произошла следующая ошибка: {e}", "state": 0}, status=400)

        if instance.status != "new":
            return Response({"message": "Объект прошел стадию модерации, изменить невозможно",
                             "state": 0}, status=400)
        else:
            serializer = MountainPassEditSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"state": 1}, status=200)
