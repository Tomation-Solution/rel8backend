import django_filters
from . import models

class MeetingFitlter(django_filters.FilterSet):
    council = django_filters.NumberFilter(field_name='exco')
    # if exco is none meaning it is formembers
    for_members = django_filters.BooleanFilter(field_name='exco', lookup_expr='isnull')
    is_for_all_grade = django_filters.BooleanFilter(field_name='membership_grade', lookup_expr='isnull')

    chapters = django_filters.NumberFilter(field_name='chapters')
    commitee = django_filters.NumberFilter()
    class Meta:
        model = models.Meeting
        fields = [
            'exco','chapters','membership_grade','commitee','for_members'
        ]
