from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestDriveViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'test-drive', TestDriveViewSet, basename='test-drive')
router.register(r'reserve', ReservationViewSet, basename='reserve')

urlpatterns = [
    path('', include(router.urls)),
]
