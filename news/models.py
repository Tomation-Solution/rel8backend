from email.policy import default
from django.db import models
from account.models import user as user_models
from utils.custom_exceptions import CustomError
from account.models import auth as auth_realted_models
from account.models import user as user_realted_models
from django.conf import settings

# Create your models here.




class News(models.Model):
    name = models.CharField(max_length=300)
    is_exco = models.BooleanField(default=False)
    is_committe = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    commitee_name = models.ForeignKey(user_models.CommiteeGroup,null=True,on_delete=models.CASCADE,blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True,blank=True)
    body = models.TextField(default=" ")
    image = models.ImageField(upload_to="newsImage/%d/",null=True,default=None)
    user_that_have_reacted = models.ManyToManyField(user_realted_models.Memeber,blank=True)
    danload = models.FileField(upload_to='newsFileDanload/%d/',null=True,default=None)
    exco = models.ForeignKey(user_models.ExcoRole,on_delete=models.SET_NULL,null=True,default=None,blank=True) 
    dues_for_membership_grade  =models.ForeignKey(user_models.MemberShipGrade,on_delete=models.SET_NULL,null=True,default=None,blank=True)
    
    def __str__(self):return self.name
    
    def save(self, *args,**kwargs) -> None:
        if self.is_committe:
            if self.commitee_name is None:raise CustomError({"error":"if you choose committee you must pick the commitee name"})
        return super().save(*args,**kwargs)

    def get_image_url(self):
        return'{}{}'.format(settings.CLOUDINARY_ROOT_URL,self.image)





class NewsParagraph(models.Model):
    news = models.ForeignKey(News,on_delete=models.CASCADE)
    paragragh = models.TextField(default=' ',null=True,blank=True)
    heading = models.TextField(default=' ',null=True,blank=True)



class NewsComment(models.Model):
    news = models.ForeignKey(News,on_delete=models.CASCADE)
    # member that commented
    member = models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE)
    comment = models.TextField()