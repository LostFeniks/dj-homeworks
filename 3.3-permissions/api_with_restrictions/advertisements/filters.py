import django_filters
from django_filters import rest_framework as filters
from .models import Advertisement

class AdvertisementFilter(filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    status = django_filters.CharFilter(field_name='status')
    creator_id = django_filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator_id']
