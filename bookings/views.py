from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TestDrive, Reservation
from .serializers import TestDriveSerializer, ReservationSerializer

class TestDriveViewSet(viewsets.ModelViewSet):
    serializer_class = TestDriveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return TestDrive.objects.all().order_by('-created_at')
        return TestDrive.objects.filter(user=self.request.user).order_by('-created_at')


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all().order_by('-reserved_at')
        return Reservation.objects.filter(user=self.request.user).order_by('-reserved_at')
