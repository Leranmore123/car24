from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarInquiryViewSet

router = DefaultRouter()
router.register(r'inquiry', CarInquiryViewSet, basename='inquiry')

urlpatterns = [
    path('', include(router.urls)),
]
