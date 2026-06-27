from django.contrib import admin
from .models import TestDrive, Reservation

class TestDriveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'date', 'time_slot', 'location_type', 'status', 'created_at')
    list_filter = ('location_type', 'status', 'date')
    search_fields = ('user__username', 'car__brand', 'car__model')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'amount_paid', 'status', 'reserved_at', 'expiry_date')
    list_filter = ('status', 'reserved_at')
    search_fields = ('user__username', 'car__brand', 'car__model')

admin.site.register(TestDrive, TestDriveAdmin)
admin.site.register(Reservation, ReservationAdmin)
