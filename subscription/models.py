from django.db import models,connection
from Rel8Tenant import models as tenant_models
from account.models import user as user_model
from utils.usefulFunc import get_localized_time
from django_celery_beat.models import (
    PeriodicTask,ClockedSchedule
)
from utils.custom_exceptions import CustomError
from datetime import date,datetime,timedelta
import json


# Create your models here.
"depending on the models.Model payment_plan we use that to check the Subscription models if there any is_end=False"
"""
So hear is the 


to check if the person has paid we use login so we would have expire logini
"""


# class SubScriptionTimerSetter:


"on Succeful Payment we use the signal to crete a one off Subsription Timer with celery for 1 year"
class TenantSubscription(models.Model):
    tenant = models.ForeignKey(tenant_models.Client,on_delete=models.CASCADE)
    is_paid_succesfully =models.BooleanField(default=False)
    paystack_key = models.CharField(max_length=100)
    is_end  = models.BooleanField(default=False)

class IndividualSubscription(models.Model):
    paystack_key = models.CharField(max_length=100)
    is_end  = models.BooleanField(default=False)
    member = models.ForeignKey(user_model.Memeber,on_delete=models.CASCADE)
    is_paid_succesfully =models.BooleanField(default=False)






def setTimer(id,subType,schema_name,currentTenant):
    """
    this function set the timer to 1 year before we subscribe again but we can scale the funtion to per 6,4,3 month e.t.c,
    """
    # Note subType means subcription Type
    connection.set_schema(schema_name=schema_name)
        
    if PeriodicTask.objects.all().filter(name=f"{subType} {str(id)}").exists():
        raise CustomError({"error":"Try another name this name has been taken"})
    tenant = connection.tenant

    print({"tenant":tenant})
    
    time =datetime.strptime('09:30', '%H:%M').time()
    localized_time = get_localized_time(
    #this would work 365 days
    date.today()+timedelta(days=1),time,currentTenant.timezone
    )
    clocked, _ = ClockedSchedule.objects.get_or_create(
        clocked_time=localized_time
        )

    PeriodicTask.objects.create(
        clocked=clocked,
        name = f"Payment for {subType} {id}",
        task = "",#this is the task i would want to trigger it would just some couple boolean
        args=json.dumps(
                [
                    id,
                    subType,
                ]
            ),  # arguments
        headers=json.dumps(
                {
                    "_schema_name": schema_name,
                    "_use_tenant_timezone": True,
                }
            ),
            one_off=True
    )


"""
Organisation Subscription

Individual  Subscription

Once a org is created Depending on the sub type they use
if it org sub:
    we give the org 7 days free trial and they can pay in between to start using paid plan
    we create a periodic task to count 1 year before we set the sub is_end=True

if it individual
we give the member 7 days free trial and they can pay in between to start using paid plan
"""