from . import models 
import django_filters




class GalleryV2Filter(django_filters.FilterSet):

    # date_taken= django_filters.DateFilter(field_name='date_taken')
    class Meta:
        model = models.GalleryV2
        fields = ['date_taken','chapters']