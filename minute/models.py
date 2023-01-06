from django.db import models
from account.models import auth as user_auth_related_models
# Create your models here.


class Minute(models.Model):
    file = models.FileField(upload_to="minute/%d/",null=True,default=None)
    chapter = models.ForeignKey(user_auth_related_models.Chapters,on_delete=models.SET_NULL, null=True,default=None)
    name=models.CharField(max_length=300,default=" ")

    def __str__(self):return self.name