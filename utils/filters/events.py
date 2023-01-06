import django_filters
from account.models import auth as auth_related_models 
from event import models as event_related_models


class EventFilter(django_filters.FilterSet):
    by_chapter = django_filters.CharFilter(
        field_name = "is_for_chapters__name"
    )

    class Meta:
        model =event_related_models.Event
        fields =[
            "is_for_chapters__name"
        ]