import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    rooms_min = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    rooms_max = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    
    class Meta:
        model = Property
        fields = ['city', 'property_type', 'deal_type', 'status']