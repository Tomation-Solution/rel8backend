from django.db import models
from account.models import user as user_models
from account.models import auth as auth_models
# Create your models here.
from cloudinary_storage.storage import RawMediaCloudinaryStorage



class Meeting(models.Model):
    name = models.TextField(default='')
    details = models.TextField(default='..')
    exco = models.ForeignKey(user_models.ExcoRole,null=True ,default=None,on_delete=models.SET_NULL,blank=True)
    chapters = models.ForeignKey(auth_models.Chapters,null=True ,default=None,on_delete=models.SET_NULL,blank=True)
    membership_grade  = models.ForeignKey(user_models.MemberShipGrade,null=True ,default=None,on_delete=models.SET_NULL,blank=True)
    date_for = models.DateTimeField(null=True,default=None)
    addresse = models.TextField(default='')
    event_date = models.DateTimeField(null=True,default=None)
    commitee = models.ForeignKey(user_models.CommiteeGroup,null=True,on_delete=models.CASCADE,blank=True,default=None)

    organiserName =models.CharField(max_length=400,default='')
    organiserDetails =models.CharField(max_length=400,default='')
    organiserImage = models.ImageField(default=None,null=True,upload_to='meeting_organiser/%d/')

    meeting_docs = models.FileField(upload_to='meeting_docs/%d/',null=True,default=None,
        storage=RawMediaCloudinaryStorage(),
    )

    def __str__(self):
        return self.name

class MeetingAttendies(models.Model):
    members = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,null=True ,default=None,)

class MeetingProxyAttendies(models.Model):
    member = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE)
    # {
    #     full_name:string;
    #     email:string
    # }
    # {'participants':[]}
    participants  = models.JSONField(default=dict)

class MeetingReshedule(models.Model):
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,null=True ,default=None,)
    members = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    request_reschedule_date =models.DateTimeField(null=True,default=None)


class MeetingApology(models.Model):
    'people that can attend'
    members = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting,on_delete=models.CASCADE,null=True ,default=None,)
    note = models.TextField(default='I sorry i can attend')
