import django_filters
from django.db.models import Q

class AdminCommentFilter(django_filters.FilterSet):
    status = django_filters.CharFilter('status', method='status_filter')
    q = django_filters.CharFilter(field_name="text", method='query_all_words')
    
    def status_filter(self, queryset, name, value):
        if value == "all":
            return queryset
        elif value == "approved":
            return queryset.filter(is_approved=True)
        elif value == "unapproved":
            return queryset.filter(is_approved=False)
        else:
            return queryset
    
    def query_all_words(self, queryset, name, value):
        if not value:
            return queryset

        terms = [term.strip() for term in value.split() if term.strip()]
        if not terms:
            return queryset

        combined_q = Q()

        for term in terms:
            combined_q |= Q(text__icontains=term)

        return queryset.filter(combined_q).distinct()