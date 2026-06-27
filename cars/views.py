from rest_framework import viewsets, filters, permissions
from django_filters import rest_framework as django_filters
from .models import Car
from .serializers import CarSerializer

class CarFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_year = django_filters.NumberFilter(field_name="year", lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name="year", lookup_expr='lte')
    min_km = django_filters.NumberFilter(field_name="km_driven", lookup_expr='gte')
    max_km = django_filters.NumberFilter(field_name="km_driven", lookup_expr='lte')

    brand = django_filters.CharFilter(method='filter_brand')
    city = django_filters.CharFilter(method='filter_city')
    model = django_filters.CharFilter(field_name="model", lookup_expr='icontains')
    status = django_filters.CharFilter(field_name="status", lookup_expr='iexact')
    fuel_type = django_filters.CharFilter(field_name="fuel_type", lookup_expr='iexact')
    transmission = django_filters.CharFilter(field_name="transmission", lookup_expr='iexact')
    body_type = django_filters.CharFilter(field_name="body_type", lookup_expr='iexact')

    class Meta:
        model = Car
        fields = []

    def filter_brand(self, queryset, name, value):
        if not value:
            return queryset
        from django.db.models import Q
        # Split by words to handle 'Maruti Suzuki' vs 'maruti'
        words = value.lower().split()
        q_obj = Q()
        for word in words:
            if len(word) > 2:
                q_obj |= Q(brand__icontains=word)
        if not q_obj:
            q_obj = Q(brand__icontains=value)
        return queryset.filter(q_obj)

    def filter_city(self, queryset, name, value):
        if not value:
            return queryset
        val_lower = value.lower().strip()
        from django.db.models import Q
        if 'bangalore' in val_lower or 'bengaluru' in val_lower or 'bagluru' in val_lower:
            return queryset.filter(Q(city__iexact='bangalore') | Q(city__iexact='bengaluru') | Q(city__iexact='bagluru'))
        if 'ahmedabad' in val_lower or 'ahmadvad' in val_lower or 'ahm' in val_lower:
            return queryset.filter(Q(city__iexact='ahmedabad') | Q(city__iexact='ahmadvad'))
        return queryset.filter(city__iexact=value)

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by('-created_at')
    serializer_class = CarSerializer
    filterset_class = CarFilter
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand', 'model', 'variant', 'city', 'location_hub']
    ordering_fields = ['price', 'year', 'km_driven', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        car = serializer.save()
        from .models import InspectionReport
        # Generate a default inspection report for the new car listing
        InspectionReport.objects.create(
            car=car,
            overall_rating=4.5,
            engine_rating=4.5,
            exterior_rating=4.5,
            interior_rating=4.5,
            suspension_rating=4.5,
            brakes_rating=4.5,
            inspector_notes="Inspection successfully passed. Evaluated by CarBazaar."
        )
