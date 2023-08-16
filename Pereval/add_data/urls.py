from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'coordinates', CoordinatesViewSet)
router.register(r'images', ImageViewSet)
router.register(r'users', UserViewSet)
router.register(r'passes', PassViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/submitData/', MountainPassAddView.as_view(), name='submitData'),
    path('api/submitData/<int:pk>/', MountainPassEditView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]