import django_filters
from . import models

class MeetingFitlter(django_filters.FilterSet):
    exco = django_filters.NumberFilter()
    # chapters = django_filters.BooleanFilter(field_name='chapters', lookup_expr='isnull')
    # if exco is none meaning it is formembers
    for_members = django_filters.BooleanFilter(field_name='exco', lookup_expr='isnull')

    class Meta:
        model = models.Meeting
        fields = [
            'exco','chapters','for_members'
        ]