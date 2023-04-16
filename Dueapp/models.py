from django.db import models, connection
import json
from django_celery_beat.models import  (
    PeriodicTask,CrontabSchedule,
    IntervalSchedule,ClockedSchedule )
from django.contrib.auth import get_user_model
from account.models import user as user_model
from utils.custom_exceptions import CustomError
from utils.usefulFunc import get_localized_time
from account.models import auth as auth_realted_models
from .tasks import create_deactivating_user_model
from django.shortcuts import get_object_or_404

def convert12Hour(hour):
    'convert 12 hrs to 24 hr for e.g we have 13hr the function returns 1'
    if hour == 13:hour =1
    if hour ==14:hour =2
    if hour ==15:hour =3
    if hour ==16:hour =4
    if hour ==17:hour =5
    if hour ==18:hour =6
    if hour ==19:hour =7
    if hour ==20:hour =8
    if hour ==21:hour =9
    if hour ==22:hour =10
    if hour ==23:hour =11
    if hour ==24:hour =12

    return hour

class Due(models.Model):
    #after creation celery will take it from here by creating the Due_User Object it self
    class ScheduleTypes(models.TextChoices):
        day_of_week='day_of_week'
        month_of_year="month_of_year"
    Name = models.CharField(max_length=355)
    re_occuring= models.BooleanField(default=False)# due_type Once  Re-occuring|
    is_for_excos = models.BooleanField(default=False)#embers | excos
    amount=  models.DecimalField(decimal_places=4,max_digits=19,default=0.00)
    exco = models.ForeignKey(user_model.ExcoRole,default=None,null=True,on_delete=models.CASCADE)
    # for once there must be a startDate
    startDate =models.DateField(null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
    # for is re-occuring there must be a startDate and endDate
    endDate =models.DateField(null=True, blank=True)
    endTime =models.TimeField(null=True, blank=True)
    scheduletype = models.CharField(choices=ScheduleTypes.choices,default='day_of_week',max_length=200)
    schedule = models.JSONField(null=True,default=None)
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True,blank=True)
    alumni_year = models.DateField(default=None,null=True,blank=True)
    dues_for_membership_grade  =models.ForeignKey(user_model.MemberShipGrade,on_delete=models.SET_NULL,null=True,default=None,blank=True)
    # this will be manual the date dont really matter it charges the  person on when the manully_create_due_job is manually called e.g(when a member is create)
    is_on_create = models.BooleanField(default=False)
    is_deactivate_users =models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.Name

    def save(self, *args,**kwargs) -> None:
        return super().save(*args,**kwargs)
        # self.create_due_job()
        # return saved

    
    def create_due_job(self):
        "this fucntion create a cron job that helps to create due for the users"
        # day_of_week-0,1 - means run sunday and monday
        # month_of_year0-1,2,3 means run jan feb march
        print("called")
        tenant = connection.tenant
        # if self.is_on_create:
        #     print('Dont do shit... this gives the power of charging the user to the logic not celery')
        # else:
            # if PeriodicTask.objects.all().filter(name=f"{self.Name} {str(self.id)}").exists():
            #     raise CustomError({"error":"Try another name this name has been taken"})
            # if self.re_occuring:
            #     if self.schedule == None:
            #         # ["2","3"] should be like this
            #         raise CustomError({'error':"schedule must be a array of numberString"})
            #     # self.startDate Note this is a date object
            #     if(self.scheduletype == 'day_of_week'):            
            #         schedule,_ =CrontabSchedule.objects.get_or_create(
            #             day_of_week=','.join( self.schedule),
            #     hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,#means it will work on 8:30, of each day of week u choose

            #         )
            #     if(self.scheduletype =='month_of_year'):
            #         schedule,_ =CrontabSchedule.objects.get_or_create(
            #         hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,#means it will work on 8:30, month of year u choose
            #                     month_of_year=','.join( self.schedule)
            #             )
                
            #     chapterID = None
            #     if self.chapters:chapterID=self.chapters.id
            #     PeriodicTask.objects.create(
            #         crontab=schedule,
            #         name=f"{self.Name} {str(self.id)}",  # task name
            #         task="Dueapp.tasks.create_due_job",   # task.
            #         args=json.dumps(
            #             [
            #                 self.id,
            #             chapterID
            #             ]
            #         ),  # arguments
            #         description="this changes the task status to active at start time",
            #         one_off=False,
            #         headers=json.dumps(
            #             {
            #                 "_schema_name": tenant.schema_name,
            #                 "_use_tenant_timezone": True,
            #             }
            #         ),
            #     )
            # else:
        chapterID=None
        if self.chapters:chapterID=self.chapters.id

        if self.is_on_create == False:
            "if is_on_create == True ... it means this user is wants to handle the due_user creation"
            tenant = connection.tenant
            localized_time = get_localized_time(
                self.startDate, self.startTime, tenant.timezone
            )
            clocked, _ = ClockedSchedule.objects.get_or_create(
            clocked_time=localized_time
            )
            chapterID = None
            PeriodicTask.objects.create(
            clocked=clocked,
                name=f"{self.Name} {str(self.id)}",  # task name
                task="Dueapp.tasks.create_due_job",  # task.
                args=json.dumps(
                [
                self.id,
                chapterID
                ]
                ),  # arguments
                description="this changes the task status to active at start time",
                one_off=True,
                headers=json.dumps(
                {
                "_schema_name": tenant.schema_name,
                "_use_tenant_timezone": True,
                }
                )
            )

        if self.is_deactivate_users:
                localized_time = get_localized_time(self.endDate, self.endTime, tenant.timezone
                )
                clocked, _ = ClockedSchedule.objects.get_or_create(
                clocked_time=localized_time
                )

                PeriodicTask.objects.create(
                clocked=clocked,
                    name=f"{self.Name} {str(self.id)} set owing members to is_financial=false",  # task name
                    task="Dueapp.tasks.deactivate_owing_members",  # task.
                    args=json.dumps(
                    [
                    self.id,
                    chapterID
                    ]
                    ),  # arguments
                    description="set owing members to is_financial=false",
                    one_off=True,
                    headers=json.dumps(
                    {
                    "_schema_name": tenant.schema_name,
                    "_use_tenant_timezone": True,
                    }
                    )
                )

class Due_User(models.Model):
    #To get how much the user is owing we query useing the user object and the is_paid
    user=models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,null=True)
    due = models.ForeignKey(Due,on_delete=models.CASCADE)
    is_overdue = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    amount= models.DecimalField(decimal_places=2,max_digits=10)
    paystack_key = models.TextField(default='')




    def __str__(self) -> str:
        try:
            return f'{self.user.email} {self.due.Name}'
        except:
            return  f' {self.due.Name}'



class DeactivatingDue(models.Model):
    "if u dont pay this due u are going to be lock out"
    name = models.CharField(max_length=355)
    is_for_excos = models.BooleanField(default=False)#embers | excos
    amount=  models.DecimalField(decimal_places=2,max_digits=19,default=0.00)
    # for once there must be a startDate
    startDate =models.DateField(null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
    # for is re-occuring there must be a startDate and endDate
    endDate =models.DateField(null=True, blank=True)
    month = models.JSONField(null=True)
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True)




    def deactivating_due_job(self):
        tenant = connection.tenant
        # first we have to create all the dues for the user then activate the perodic task...
        # it the perodic task once activated will check if people have paid if not we deactivate the user knowing fully well
        if PeriodicTask.objects.all().filter(name=f"{self.name} {str(self.id)}").exists():
            raise CustomError({"error":"Try another name this name has been taken"})

        schedule,_ =CrontabSchedule.objects.get_or_create(
            month_of_year=self.month,
            hour=convert12Hour(self.startTime.hour), minute=self.startTime.minute,

        )
        # localized_time = get_localized_time(
        #     self.startDate, self.startTime, tenant.timezone
        # )
        chapterID = None
        if self.chapters:chapterID=self.chapters.id
        create_deactivating_user_model(self.id,chapterID)

        PeriodicTask.objects.create(
                crontab=schedule,
                name=f"{self.name} {str(self.id)}",  # task name
                task="Dueapp.tasks.deactivating_due_job",   # task.
                args=json.dumps(
                    [
                        self.id,
                        chapterID
                    ]
                ),  # arguments
                description="this will check",
                one_off=True,
                headers=json.dumps(
                    {
                        "_schema_name": tenant.schema_name,
                        "_use_tenant_timezone": True,
                    }
                ),
            )


class DeactivatingDue_User(models.Model):
    #To get how much the user is owing we query useing the user object and the is_paid
    user=models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,null=True)
    deactivatingdue = models.ForeignKey(DeactivatingDue,on_delete=models.CASCADE)
    is_overdue = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    amount= models.DecimalField(decimal_places=2,max_digits=10)
    paystack_key = models.TextField(default='')




    def __str__(self) -> str:
        return f'{self.user.email} {self.deactivatingdue.name}'

