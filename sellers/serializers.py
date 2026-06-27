from rest_framework import serializers
from .models import CarInquiry
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

class CarInquirySerializer(serializers.ModelSerializer):
    admin_commission = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    main_image = serializers.ImageField(required=False, allow_null=True)
    video = serializers.FileField(required=False, allow_null=True)
    user_detail = UserSerializer(source='user', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        required=False, 
        write_only=True,
        allow_null=True
    )

    class Meta:
        model = CarInquiry
        fields = [
            'id', 'brand', 'model', 'year', 'km_driven', 'fuel_type', 
            'transmission', 'expected_price', 'contact_name', 'contact_phone', 
            'city', 'preferred_inspection_date', 'status', 'admin_commission', 
            'main_image', 'video', 'created_at', 'user_detail', 'user_id'
        ]
        read_only_fields = ['status', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        is_staff = request and request.user and request.user.is_staff
        if is_staff:
            if 'status' in self.fields:
                self.fields['status'].read_only = False
        else:
            # Securely remove commission field for regular users
            self.fields.pop('admin_commission', None)

    def create(self, validated_data):
        request = self.context.get('request')
        user = validated_data.get('user')
        if not user and request and request.user.is_authenticated:
            user = request.user
        return CarInquiry.objects.create(user=user, **validated_data)
