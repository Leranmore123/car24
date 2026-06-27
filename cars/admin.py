from django.contrib import admin
from .models import Car, CarImage, InspectionReport

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class InspectionReportInline(admin.StackedInline):
    model = InspectionReport

class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'year', 'price', 'fuel_type', 'transmission', 'city', 'status')
    list_filter = ('brand', 'fuel_type', 'transmission', 'city', 'status')
    search_fields = ('brand', 'model', 'city')
    inlines = [CarImageInline, InspectionReportInline]

admin.site.register(Car, CarAdmin)
admin.site.register(CarImage)
admin.site.register(InspectionReport)
