import django_filters
from . import models

class PublicationLookUp(django_filters.FilterSet):

    'to seach by council for_members has to be false'
    council = django_filters.NumberFilter(field_name='exco')
    for_members = django_filters.BooleanFilter(field_name='exco', lookup_expr='isnull')

    'to seach by membership_grade is_for_all_grade has to be false'
    is_for_all_grade = django_filters.BooleanFilter(field_name='membership_grade', lookup_expr='isnull')
    membership_grade = django_filters.NumberFilter()
    chapters = django_filters.NumberFilter(field_name='chapters')
    commitee = django_filters.NumberFilter(field_name='commitee_name')


    class Meta:
        model = models.Publication
        fields =[ 'membership_grade','is_for_all_grade','council','for_members','chapters','commitee']
