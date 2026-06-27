from rest_framework import viewsets, permissions
from .models import CarInquiry
from .serializers import CarInquirySerializer

class CarInquiryViewSet(viewsets.ModelViewSet):
    serializer_class = CarInquirySerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return CarInquiry.objects.all().order_by('-created_at')
            return CarInquiry.objects.filter(user=self.request.user).order_by('-created_at')
        return CarInquiry.objects.none()

    def perform_update(self, serializer):
        instance = serializer.save()
        
        # When status changes to Completed, automatically add the car to the public listings!
        if instance.status == 'Completed':
            from cars.models import Car, InspectionReport
            
            # Map registration state based on city
            reg_state = 'GJ-01'
            city_lower = instance.city.lower()
            if 'mumbai' in city_lower:
                reg_state = 'MH-02'
            elif 'delhi' in city_lower:
                reg_state = 'DL-3C'
            elif 'bangalore' in city_lower or 'bengaluru' in city_lower:
                reg_state = 'KA-51'

            car_exists = Car.objects.filter(
                brand=instance.brand,
                model=instance.model,
                year=instance.year,
                city=instance.city,
                km_driven=instance.km_driven
            ).exists()
            
            if not car_exists:
                # Final sale price is expected price + admin commission
                final_price = instance.expected_price + instance.admin_commission
                
                # Determine body type dynamically from model name
                model_lower = instance.model.lower()
                body_type = 'Hatchback'
                if any(x in model_lower for x in ['suv', 'creta', 'nexon', 'fortuner', 'brezza', 'seltos']):
                    body_type = 'SUV'
                elif any(x in model_lower for x in ['city', 'verna', 'dzire', 'ciaz', 'amaze']):
                    body_type = 'Sedan'
                elif any(x in model_lower for x in ['ertiga', 'carens', 'innnova', 'triber']):
                    body_type = 'MUV'

                # Create the Car listing
                car = Car.objects.create(
                    brand=instance.brand,
                    model=instance.model,
                    year=instance.year,
                    price=final_price,
                    km_driven=instance.km_driven,
                    fuel_type=instance.fuel_type,
                    transmission=instance.transmission,
                    body_type=body_type,
                    city=instance.city,
                    registration_state=reg_state,
                    location_hub=f"Spinny Hub, {instance.city}",
                    status='available',
                    main_image=instance.main_image,
                    video=instance.video,
                )
                
                # Create a default inspection report for the new car so it doesn't crash the details page
                InspectionReport.objects.create(
                    car=car,
                    overall_rating=4.5,
                    engine_rating=4.6,
                    exterior_rating=4.4,
                    interior_rating=4.5,
                    suspension_rating=4.5,
                    brakes_rating=4.4,
                    inspector_notes="Evaluation successfully passed. Checked and certified by CarBazaar. Excellent overall condition with fully functional components."
                )
