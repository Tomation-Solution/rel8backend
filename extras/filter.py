from . import models 
import django_filters




class GalleryV2Filter(django_filters.FilterSet):
    not_chapters  = django_filters.BooleanFilter(field_name='chapters',lookup_expr='isnull')

    # date_taken= django_filters.DateFilter(field_name='date_taken')
    class Meta:
        model = models.GalleryV2
        fields = ['date_taken','chapters','not_chapters']