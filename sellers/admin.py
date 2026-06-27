from django.contrib import admin
from .models import CarInquiry

class CarInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_name', 'brand', 'model', 'year', 'expected_price', 'city', 'status', 'admin_commission', 'created_at')
    list_filter = ('status', 'city', 'created_at')
    search_fields = ('contact_name', 'contact_phone', 'brand', 'model')

admin.site.register(CarInquiry, CarInquiryAdmin)
