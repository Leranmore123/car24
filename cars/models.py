from django.db import models

class Car(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]
    
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]
    
    BODY_CHOICES = [
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('MUV', 'MUV'),
        ('Luxury', 'Luxury'),
    ]

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    variant = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    km_driven = models.IntegerField()
    fuel_type = models.CharField(max_length=15, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=15, choices=TRANSMISSION_CHOICES)
    body_type = models.CharField(max_length=20, choices=BODY_CHOICES)
    owner_count = models.IntegerField(default=1) # 1 = First Owner, 2 = Second Owner, etc.
    registration_state = models.CharField(max_length=10) # e.g. "GJ-01", "DL-3C"
    city = models.CharField(max_length=50) # Ahmedabad, Delhi, Mumbai, Bangalore
    location_hub = models.CharField(max_length=100) # e.g., "Spinny Hub, Vastrapur"
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    image_url = models.URLField(max_length=500, blank=True, null=True) # Direct URLs for seeding
    main_image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    video_url = models.URLField(max_length=500, blank=True, null=True) # Direct URL for seeding video
    video = models.FileField(upload_to='car_videos/', blank=True, null=True)
    
    # Tech specifications
    mileage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="kmpl or km/kg")
    engine_displacement = models.IntegerField(blank=True, null=True, help_text="in cc")
    max_power = models.CharField(max_length=50, blank=True, null=True) # e.g. "81.86 bhp @ 6000 rpm"
    torque = models.CharField(max_length=50, blank=True, null=True) # e.g. "113.75 Nm @ 4000 rpm"
    seats = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} ({self.variant or ''})"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='car_images/gallery/', blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.car}"


class InspectionReport(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='inspection_report')
    
    # Summary overall rating out of 5 stars
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    
    # 5-star ratings for components
    engine_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    exterior_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    interior_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    suspension_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    brakes_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    
    # Checklist details (boolean values)
    engine_sound_ok = models.BooleanField(default=True)
    exhaust_smoke_ok = models.BooleanField(default=True)
    clutch_gear_ok = models.BooleanField(default=True)
    ac_cooling_ok = models.BooleanField(default=True)
    steering_ok = models.BooleanField(default=True)
    suspension_sound_ok = models.BooleanField(default=True)
    tyres_ok = models.BooleanField(default=True)
    airbags_intact = models.BooleanField(default=True)
    
    inspector_notes = models.TextField(blank=True, null=True)
    inspected_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Inspection for {self.car} - Rating: {self.overall_rating}"
