from django.db import models
from account.models import user as user_models
from utils.custom_exceptions import CustomError
from account.models import auth as auth_realted_models
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here.


class Publication(models.Model):
    name = models.CharField(max_length=300)
    is_exco = models.BooleanField(default=False)
    exco = models.ForeignKey(user_models.ExcoRole,on_delete=models.SET_NULL,null=True,default=None,blank=True) 
    is_committe = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    commitee_name = models.ForeignKey(user_models.CommiteeGroup,null=True,on_delete=models.CASCADE,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    body = models.TextField(default=" ")
    image = models.ImageField(upload_to="newsImage/%d/",null=True,default=None)
    danload = models.FileField(upload_to='newsFileDanload/%d/',null=True,default=None,
        storage=RawMediaCloudinaryStorage(),
    )
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True,blank=True)
    membership_grade  = models.ForeignKey(user_models.MemberShipGrade,null=True ,default=None,on_delete=models.SET_NULL,blank=True)

    def __str__(self):return self.name
    
    def save(self, *args,**kwargs) -> None:
        if self.is_committe:
            if self.commitee_name is None:raise CustomError({"error":"if you choose committee you must pick the commitee name"})
        return super().save(*args,**kwargs)


class PublicationParagraph(models.Model):
    publication = models.ForeignKey(Publication,on_delete=models.CASCADE)
    paragragh = models.TextField(default=' ',null=True,blank=True)
    heading = models.TextField(default=' ',null=True,blank=True)



class PublicationComment(models.Model):
    news = models.ForeignKey(Publication,on_delete=models.CASCADE)
    # member that commented
    member = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    comment = models.TextField()