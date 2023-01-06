from . import models 
import django_filters
from account.models.auth import Chapters




class RescheduleEventRequestFilter(django_filters.FilterSet):
    # event = django_filters.CharFilter(
    #     field_name="event__id",max_length=255
    # )

    class Meta:
        model = models.RescheduleEventRequest
        fields= ['event','startDate','startTime']



class EventLookUp(django_filters.FilterSet):
    exco = django_filters.NumberFilter(field_name='exco__id')
    exco_name = django_filters.CharFilter(field_name='exco__name')
    filter_by_chapters= django_filters.NumberFilter(field_name='chapters__id')
    class Meta:
        model = models.Event
        fields =['exco','exco_name','filter_by_chapters',]