from django.db import models




class LastestUpdates(models.Model):
    title = models.TextField()
    body = models.TextField()
    image = models.ImageField(upload_to='latest_update/%d/',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title