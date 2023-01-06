from datetime import datetime, timedelta, date, time, timezone
from django.utils import timezone


def get_localized_time(date: date, time: time, timezone: timezone) -> datetime:
    """Returns a localized date time"""
    return timezone.localize(datetime.combine(date, time))


def convert_naira_to_kobo(naira):
    naira = float(naira)*100
    kobo = int(naira)
    return kobo
