import django_filters
from . import models

class NewsLookUp(django_filters.FilterSet):

    # exco = django_filters.NumberFilter(field_name='exco__id')
    # exco_name = django_filters.CharFilter(field_name='exco__name')
    # filter_by_chapters= django_filters.NumberFilter(field_name='chapters__id')


    "this is inline witht the meeting look up"

    council = django_filters.NumberFilter(field_name='exco')

    is_for_all_grade = django_filters.BooleanFilter(field_name='dues_for_membership_grade', lookup_expr='isnull')
    
    not_council = django_filters.BooleanFilter(field_name='exco', lookup_expr='isnull')
    not_commitee  = django_filters.BooleanFilter(field_name='commitee_name',lookup_expr='isnull')
    not_chapters  = django_filters.BooleanFilter(field_name='chapters',lookup_expr='isnull')

    membership_grade = django_filters.NumberFilter(field_name='dues_for_membership_grade',)
    commitee = django_filters.NumberFilter(field_name='commitee_name')
    chapters = django_filters.NumberFilter(field_name='chapters')

    class Meta:
        model = models.News
        fields =[ 'membership_grade','is_for_all_grade','council','commitee','chapters','not_commitee']

