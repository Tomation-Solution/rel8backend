from django.db import models
from account.models import auth as auth_realted_models
from account.models import user as user_realted_models




class Gallery(models.Model):
    link = models.TextField()
    photo_file = models.ImageField(upload_to="gallery/")
    name = models.CharField(max_length=300)
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True,blank=True,default=None)


    def __str__(self):return self.name

class Ticketing(models.Model):
    heading = models.CharField(max_length=300)
    body =  models.TextField()

    def __str__(self):return self.heading




class GalleryV2(models.Model):
    name = models.TextField()
    date_taken = models.DateField()
    chapters = models.ForeignKey(auth_realted_models.Chapters,on_delete=models.SET_NULL,null=True,blank=True,default=None)


class ImagesForGalleryV2(models.Model):
    image =  models.ImageField(upload_to="gallery_v2/")
    gallery = models.ForeignKey(GalleryV2,on_delete=models.CASCADE,)


class FundAProject(models.Model):
    heading =models.CharField(max_length=50)
    about = models.TextField(default='')
    amount_made =models.DecimalField(decimal_places=2,max_digits=10,default=0.00)


class SupportProjectInCash(models.Model):
    member = models.ForeignKey(user_realted_models.Memeber,null=True,default=True,on_delete=models.CASCADE)
    amount= models.DecimalField(decimal_places=2,max_digits=10)
    paystack_key = models.TextField(default='')
    is_paid = models.BooleanField(default=False)
    project = models.ForeignKey(FundAProject,null=True,default=True,on_delete=models.CASCADE)

class SupportProjectInKind(models.Model):
    member = models.ForeignKey(user_realted_models.Memeber,null=True,default=True,on_delete=models.CASCADE)
    heading =models.CharField(max_length=50)
    about = models.TextField(default='')
    project = models.ForeignKey(FundAProject,null=True,default=True,on_delete=models.CASCADE)
