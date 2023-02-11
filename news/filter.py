import django_filters
from . import models

class NewsLookUp(django_filters.FilterSet):

    # exco = django_filters.NumberFilter(field_name='exco__id')
    # exco_name = django_filters.CharFilter(field_name='exco__name')
    # filter_by_chapters= django_filters.NumberFilter(field_name='chapters__id')


    "this is inline witht the meeting look up"

    'to seach by council for_members has to be false'
    council = django_filters.NumberFilter(field_name='exco')
    for_members = django_filters.BooleanFilter(field_name='exco', lookup_expr='isnull')

    'to seach by membership_grade is_for_all_grade has to be false'
    is_for_all_grade = django_filters.BooleanFilter(field_name='dues_for_membership_grade', lookup_expr='isnull')
    membership_grade = django_filters.NumberFilter(field_name='dues_for_membership_grade',)
    class Meta:
        model = models.News
        fields =[ 'membership_grade','is_for_all_grade','council','for_members']