import datetime
from django.db.models import Q
from django_filters.rest_framework import filterset, filters
from .models import Order

class OrderFilter(filterset.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    # start_date = filters.DateFilter("created_at", lookup_expr='gte')
    # end_date = filters.DateFilter("created_at", method='filter_end_date')
    
    # def filter_end_date(self, queryset, name, value):
    #     value = datetime.datetime.combine(value, datetime.time.max)
    #     return queryset.filter(created_at__lte=value)
    class Meta:
        model = Order
        # fields = ['status', 'start_date', 'end_date']
        fields = ['status']


class ProductFilter(filterset.FilterSet):
    title = filters.CharFilter(field_name="title", method='query_all_words')
    
    def query_all_words(self, queryset, name, value):
        if not value:
            return queryset

        terms = [term.strip() for term in value.split() if term.strip()]
        if not terms:
            return queryset

        combined_q = Q()

        for term in terms:
            combined_q |= Q(title__icontains=term)

        return queryset.filter(combined_q).distinct()