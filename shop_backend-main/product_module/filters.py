import datetime
import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    start_date = django_filters.DateFilter("created_at", lookup_expr='gte')
    end_date = django_filters.DateFilter("created_at", method='filter_end_date')
    
    def filter_end_date(self, queryset, name, value):
        value = datetime.datetime.combine(value, datetime.time.max)
        return queryset.filter(created_at__lte=value)
    class Meta:
        model = Order
        fields = ['status', 'start_date', 'end_date']