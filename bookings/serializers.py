from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import TestDrive, Reservation
from cars.models import Car
from cars.serializers import CarSerializer
from accounts.serializers import UserSerializer

class TestDriveSerializer(serializers.ModelSerializer):
    car_detail = CarSerializer(source='car', read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), source='car', write_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        required=False, 
        write_only=True
    )

    class Meta:
        model = TestDrive
        fields = ['id', 'car_id', 'car_detail', 'user_detail', 'user_id', 'date', 'time_slot', 'location_type', 'address', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user and request.user.is_staff:
            if 'status' in self.fields:
                self.fields['status'].read_only = False

    def create(self, validated_data):
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return TestDrive.objects.create(**validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    car_detail = CarSerializer(source='car', read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), source='car', write_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        required=False, 
        write_only=True
    )

    class Meta:
        model = Reservation
        fields = ['id', 'car_id', 'car_detail', 'user_detail', 'user_id', 'amount_paid', 'status', 'reserved_at', 'expiry_date']
        read_only_fields = ['status', 'reserved_at', 'expiry_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user and request.user.is_staff:
            if 'status' in self.fields:
                self.fields['status'].read_only = False

    def create(self, validated_data):
        user = validated_data.get('user')
        if not user:
            user = self.context['request'].user
        car = validated_data['car']
        
        # Mark car as reserved
        car.status = 'reserved'
        car.save()
        
        # Set expiry to 3 days from now
        expiry_date = timezone.now() + timedelta(days=3)
        
        return Reservation.objects.create(
            user=user, 
            car=car, 
            amount_paid=validated_data.get('amount_paid', 10000.00),
            expiry_date=expiry_date
        )
