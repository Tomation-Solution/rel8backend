import django_filters
from . import models

class PublicationLookUp(django_filters.FilterSet):

    exco = django_filters.NumberFilter(field_name='exco__id')
    exco_name = django_filters.CharFilter(field_name='exco__name')
    filter_by_chapters= django_filters.NumberFilter(field_name='chapters__id')
    class Meta:
        model = models.News
        fields =['exco','exco_name','filter_by_chapters',]