from django.urls import include, path
from rest_framework import routers
from . import views
from .views import CoordinatesViewSet, ImageViewSet, UserViewSet, PassViewSet, submitData

router = routers.DefaultRouter()
router.register(r'coordinates', views.CoordinatesViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'passes', views.PassViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/submit-data/', views.submitData, name='submit-data'),
]