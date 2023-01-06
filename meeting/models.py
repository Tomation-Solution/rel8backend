from django.db import models
from account.models import user as user_models
from account.models import auth as auth_models
# Create your models here.



class Meeting(models.Model):
    name = models.TextField(default='')
    details = models.TextField(default='..')
    exco = models.ForeignKey(user_models.ExcoRole,null=True ,default=None,on_delete=models.SET_NULL,blank=True)
    chapters = models.ForeignKey(auth_models.Chapters,null=True ,default=None,on_delete=models.SET_NULL,blank=True)
    date_for = models.DateTimeField(null=True,default=None)


class MeetingAttendies(models.Model):
    members = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,null=True ,default=None,)

class MeetingReshedule(models.Model):
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,null=True ,default=None,)
    members = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    request_reschedule_date =models.DateTimeField(null=True,default=None)
