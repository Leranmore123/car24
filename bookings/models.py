from django.db import models
from django.contrib.auth.models import User
from cars.models import Car

class TestDrive(models.Model):
    LOCATION_CHOICES = [
        ('Hub', 'Test Drive at Spinny Hub'),
        ('Home', 'Test Drive at Home'),
    ]
    
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    SLOT_CHOICES = [
        ('10:00 AM - 12:00 PM', '10:00 AM - 12:00 PM'),
        ('12:00 PM - 02:00 PM', '12:00 PM - 02:00 PM'),
        ('02:00 PM - 04:00 PM', '02:00 PM - 04:00 PM'),
        ('04:00 PM - 06:00 PM', '04:00 PM - 06:00 PM'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_drives')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='test_drives')
    date = models.DateField()
    time_slot = models.CharField(max_length=50, choices=SLOT_CHOICES)
    location_type = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='Hub')
    address = models.TextField(blank=True, null=True, help_text="Required if Home test drive")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Test Drive: {self.car} on {self.date}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Completed', 'Completed'), # Car bought
        ('Refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reservations')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00) # Simulated deposit
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')
    reserved_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - Reserved: {self.car} (Status: {self.status})"
