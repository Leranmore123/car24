from django.db import models
from django.contrib.auth.models import User

class CarInquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled for Inspection'),
        ('Inspected', 'Inspected'),
        ('Completed', 'Sold to Spinny'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_inquiries', blank=True, null=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    km_driven = models.IntegerField()
    fuel_type = models.CharField(max_length=15)
    transmission = models.CharField(max_length=15)
    expected_price = models.DecimalField(max_digits=12, decimal_places=2)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    preferred_inspection_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    admin_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Internal commission set by admin")
    main_image = models.ImageField(upload_to='inquiry_images/', blank=True, null=True)
    video = models.FileField(upload_to='inquiry_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.contact_name} - {self.year} {self.brand} {self.model}"
