from rest_framework import serializers
from .models import Car, CarImage, InspectionReport

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image_url', 'image']

class InspectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    inspection_report = InspectionReportSerializer(read_only=True)
    
    # Flat write-only fields for nested inspection report
    inspection_overall_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, write_only=True)
    inspection_engine_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, write_only=True)
    inspection_exterior_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, write_only=True)
    inspection_interior_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, write_only=True)
    inspection_suspension_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, write_only=True)
    inspection_brakes_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, write_only=True)
    
    inspection_engine_sound_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_exhaust_smoke_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_clutch_gear_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_ac_cooling_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_steering_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_suspension_sound_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_tyres_ok = serializers.BooleanField(required=False, write_only=True)
    inspection_airbags_intact = serializers.BooleanField(required=False, write_only=True)
    inspection_inspector_notes = serializers.CharField(required=False, write_only=True, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Car
        fields = [
            'id', 'brand', 'model', 'variant', 'year', 'price', 'km_driven', 
            'fuel_type', 'transmission', 'body_type', 'owner_count', 
            'registration_state', 'city', 'location_hub', 'status', 
            'image_url', 'main_image', 'video_url', 'video', 'mileage', 'engine_displacement', 
            'max_power', 'torque', 'seats', 'images', 'inspection_report', 
            'created_at', 'updated_at',
            # Include write-only fields
            'inspection_overall_rating', 'inspection_engine_rating', 'inspection_exterior_rating',
            'inspection_interior_rating', 'inspection_suspension_rating', 'inspection_brakes_rating',
            'inspection_engine_sound_ok', 'inspection_exhaust_smoke_ok', 'inspection_clutch_gear_ok',
            'inspection_ac_cooling_ok', 'inspection_steering_ok', 'inspection_suspension_sound_ok',
            'inspection_tyres_ok', 'inspection_airbags_intact', 'inspection_inspector_notes'
        ]

    def create(self, validated_data):
        # Extract inspection fields
        inspection_fields = {
            'overall_rating': validated_data.pop('inspection_overall_rating', 4.5),
            'engine_rating': validated_data.pop('inspection_engine_rating', 4.5),
            'exterior_rating': validated_data.pop('inspection_exterior_rating', 4.5),
            'interior_rating': validated_data.pop('inspection_interior_rating', 4.5),
            'suspension_rating': validated_data.pop('inspection_suspension_rating', 4.5),
            'brakes_rating': validated_data.pop('inspection_brakes_rating', 4.5),
            'engine_sound_ok': validated_data.pop('inspection_engine_sound_ok', True),
            'exhaust_smoke_ok': validated_data.pop('inspection_exhaust_smoke_ok', True),
            'clutch_gear_ok': validated_data.pop('inspection_clutch_gear_ok', True),
            'ac_cooling_ok': validated_data.pop('inspection_ac_cooling_ok', True),
            'steering_ok': validated_data.pop('inspection_steering_ok', True),
            'suspension_sound_ok': validated_data.pop('inspection_suspension_sound_ok', True),
            'tyres_ok': validated_data.pop('inspection_tyres_ok', True),
            'airbags_intact': validated_data.pop('inspection_airbags_intact', True),
            'inspector_notes': validated_data.pop('inspection_inspector_notes', "Evaluation successfully passed. Checked and certified by CarBazaar. Excellent overall condition with fully functional components."),
        }
        
        car = Car.objects.create(**validated_data)
        InspectionReport.objects.create(car=car, **inspection_fields)
        return car

    def update(self, instance, validated_data):
        # Extract inspection fields
        inspection_fields = {}
        keys = [
            'overall_rating', 'engine_rating', 'exterior_rating', 'interior_rating', 
            'suspension_rating', 'brakes_rating', 'engine_sound_ok', 'exhaust_smoke_ok', 
            'clutch_gear_ok', 'ac_cooling_ok', 'steering_ok', 'suspension_sound_ok', 
            'tyres_ok', 'airbags_intact', 'inspector_notes'
        ]
        for key in keys:
            val_key = f'inspection_{key}'
            if val_key in validated_data:
                inspection_fields[key] = validated_data.pop(val_key)
                
        # Update Car fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update or Create InspectionReport
        if inspection_fields:
            report, created = InspectionReport.objects.get_or_create(car=instance)
            for attr, value in inspection_fields.items():
                setattr(report, attr, value)
            report.save()
            
        return instance
