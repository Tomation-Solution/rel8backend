from email.policy import default
from django.db import models, connection
import json
from django_celery_beat.models import  (
    PeriodicTask,CrontabSchedule,
    IntervalSchedule,ClockedSchedule )
from django.contrib.auth import get_user_model
from Dueapp.models import convert12Hour
from account.models import user as user_model
from account.models import auth as auth_realted_models
from utils.custom_exceptions import CustomError
from utils.usefulFunc import get_localized_time
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from pytz import timezone
# Create your models here.

"""
here is the plan:
    admin create event
    user_type
    if it is_paid ==true:
            event_user should be created for all the member type to pay
"""
class Event(models.Model):
    name=models.CharField(max_length=355)
    class ScheduleTypes(models.TextChoices):
        day_of_week='day_of_week'
        month_of_year="month_of_year"
        day_of_month="day_of_month"#every "1"-> every monday of each month
        day_of_week_and_month_of_year='day_of_week_and_month_of_year'
        day_of_month_and_month_of_year='day_of_month_and_month_of_year'    
    is_paid_event =models.BooleanField(default=False)
    re_occuring= models.BooleanField(default=False)# due_type Once  Re-occuring|
    is_virtual=models.BooleanField(default=False)
    
    event_docs = models.FileField(upload_to='meeting_docs/%d/',null=True,default=None,
        storage=RawMediaCloudinaryStorage(),
    )
    # 
    is_for_excos = models.BooleanField(default=False)#embers | excos
    # we want to be able to filter by exco instance ....e.g president should be only able to see this thing
    exco = models.ForeignKey(user_model.ExcoRole,on_delete=models.SET_NULL,null=True,default=None,blank=True) 
    # is_commitee = models.BooleanField(default=False)
    # commitee_name = models.CharField(max_length=300,null=True,default=None)
    commitee = models.ForeignKey(user_model.CommiteeGroup,on_delete=models.CASCADE,null=True,blank=True)
    amount=  models.DecimalField(decimal_places=4,max_digits=19,default=0.00)
    is_active = models.BooleanField(default=False)
    # if it for chapters then we filter the event for only users that belongs to that chapter
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True,blank=True)
    image = models.ImageField(null=True,default=None,upload_to='events/image/')
    address = models.TextField(default=" ")

    organiser_name = models.CharField(max_length=200,default='',blank=True)
    organiser_extra_info = models.CharField(max_length=200,default='',blank=True)
    organiserImage = models.ImageField(default=None,null=True,upload_to='event_organiser/%d/')

    event_extra_details = models.TextField(default='',blank=True)
    """    
    day_of_week-0,1 - means run sunday and monday
    month_of_year0-1,2,3 means run jan feb march
    day_of_month_and_month_of_year= {
    the example below means run every monday in month of jan
    "day_of_month":1,
    "month_of_year":0
    }
    day_of_week_and_month_of_year={
       the example below  means run sunday and monday every january
        day_of_week:0,1, 
        month_of_year:0 
    }
    """
    # for once there must be a startDate
    startDate =models.DateField(null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
    # for is re-occuring there must be a startDate and endDate
    # endDate =models.DateField(null=True, blank=True)
    scheduletype = models.CharField(choices=ScheduleTypes.choices,default='day_of_week',max_length=200)
    schedule = models.JSONField(null=True)
    # mintues  = models.CharField(max_length=30)
    # hour     = models.CharField(max_length=30)
    """
    how schedule should be like
    if it day_of_week:
            schedule = [list of numbers of string]
    if it month_of_year:
            schedule = [list of numbers of string]
    if it day_of_week_and_month_of_year:
        {
            "day_of_week_and_month_of_year":[]
        }
    """


    def create_event_job(self):
        """
        once an event is created this function is runned
        re_occuring only affects activating and deactivating of meetings for re-occuring
        """
        tenant = connection.tenant
        if PeriodicTask.objects.all().filter(name=f"{self.name} {str(self.id)}").exists():
            raise CustomError({"error":"Try another name this name has been taken"})

        # localized_time = get_localized_time(
        #     self.startDate, self.startTime, tenant.timezone
        # )
        # clocked, _ = ClockedSchedule.objects.get_or_create(
        # clocked_time=localized_time
        # )
        "the schedule now works for re_occuring and once it just that once dont reapt it self it is on_off"
        local_timezone =  timezone('Africa/Lagos')
        if self.schedule == None:
            # ["2","3"] should be like this
            raise CustomError({"error":"Invalid Schedule"})
        if(self.scheduletype == 'day_of_week'):       

            schedule,_ =CrontabSchedule.objects.get_or_create(
            day_of_week=','.join( self.schedule),# of each day of week u choose
            #means it will work on hour:minutes, 
            hour=self.startTime.hour, minute=self.startTime.minute,
            timezone=local_timezone
            )  
        if(self.scheduletype =='month_of_year'):
            schedule,_ =CrontabSchedule.objects.get_or_create(
            #means it will work on hour:minutes, 
            hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,
            month_of_year=','.join( self.schedule),
            timezone=local_timezone

                )   
        if(self.scheduletype =='day_of_month'):
            schedule,_ =CrontabSchedule.objects.get_or_create(
            #means it will work on hour:minutes, 
            hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,
            day_of_month=','.join( self.schedule),
            timezone=local_timezone

                )   
        if(self.scheduletype =='day_of_month_and_month_of_year'):
            # print('hel' in list(a.keys()))
            if not ('day_of_month' in list(self.schedule.keys())):return CustomError({"error":"day_of_month is missing Inproper data"})
            if not ('month_of_year' in list(self.schedule.keys())):return CustomError({"error":"month_of_year is missing Inproper data"})


            schedule,_ =CrontabSchedule.objects.get_or_create(
            #means it will work on hour:minutes, 
            hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,
            day_of_month=','.join( self.schedule.get('day_of_month')),
            timezone=local_timezone,
            month_of_year=','.join( self.schedule.get('month_of_year')),)
        if(self.scheduletype =='day_of_week_and_month_of_year'):
            if not ('day_of_week' in list(self.schedule.keys())):return CustomError({"error":"day_of_month is missing Inproper data"})
            if not ('month_of_year' in list(self.schedule.keys())):return CustomError({"error":"month_of_year is missing Inproper data"})

            schedule,_ =CrontabSchedule.objects.get_or_create(
            #means it will work on hour:minutes, 
            timezone=local_timezone,
            hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,
            day_of_month=','.join( self.schedule.get('day_of_month')),
            day_of_week=','.join( self.schedule.get('day_of_week')),)



        if self.re_occuring:
            """
            we are setting a periodic task that allows
            the event to be active
            if u want it once it would not run this code
            """


            PeriodicTask.objects.create(
                crontab=schedule,
            #    clocked=clocked,
                name=f"{self.name} {str(self.id)} event",#task name
                task="event.tasks.activateEvent",#task.
                args=json.dumps([self.id,]),description="PeriodicTask that activate event",
                one_off=False,headers=json.dumps({"_schema_name": tenant.schema_name,"_use_tenant_timezone": True,}),)

        else:
            "This will just a One off to activate the Event"

            PeriodicTask.objects.create(
                crontab=schedule,
            #    clocked=clocked,
                name=f"{self.name} {str(self.id)} event on-off",#task name
                task="event.tasks.activateEvent",#task.
                args=json.dumps([self.id,]),
                description="PeriodicTask that activate event",
                one_off=True,
                headers=json.dumps({"_schema_name": tenant.schema_name,
                "_use_tenant_timezone": True,
                }),
                )

class EventDue_User(models.Model):
    "this would serve has paymeny history for paid event"
    user=models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,null=True)
    event =models.ForeignKey(Event,on_delete=models.CASCADE)
    amount= models.DecimalField(decimal_places=2,max_digits=10)
    # payed_for_how_many_people= models.IntegerField(default=1,blank=True)
    paystack_key = models.TextField(default='')
    is_paid = models.BooleanField(default=False)

class EventProxyAttendies(models.Model):
    event_due_user = models.ForeignKey(EventDue_User,on_delete=models.CASCADE)
    # {'participants':[]}
    participants  = models.JSONField(default=dict)

class RescheduleEventRequest(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    startDate =models.DateField(null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
