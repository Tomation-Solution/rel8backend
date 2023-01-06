from django.db import models

# Create your models here.



class FAQ(models.Model):
    name = models.CharField(max_length=300,default="")
    body = models.TextField(default="")

    def __str__(self) -> str:
        return self.name