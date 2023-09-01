from django.db import models
from account.models.user import Memeber
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.


class Rel8CustomServices(models.Model):
    service_name= models.TextField()
    intro_text = models.TextField()
    '# {“fields”:[“name of company”,”month of birth”]'
    fields_subbission = models.JSONField(default=dict)
    file_subbission = models.JSONField(default=dict)
    is_paid = models.BooleanField(default=False)
    break_down_of_payment = models.JSONField(default=dict)
    amount =models.DecimalField(decimal_places=4,max_digits=19,default=0.00)

    def str(self):return self.service_name



class Rel8CustomMemberServiceRequests(models.Model):
    class StatusCHoices(models.TextChoices):
        approved='approved'
        pending='pending'
    status = models.CharField(choices=StatusCHoices.choices,default=StatusCHoices.pending,max_length=50)
    custom_service  = models.ForeignKey(Rel8CustomServices,on_delete=models.CASCADE)
    amount =models.DecimalField(decimal_places=4,max_digits=19,default=0.00)
    paystack_key = models.TextField()
    member = models.ForeignKey(Memeber,on_delete=models.CASCADE)

class Rel8CustomMemberServiceRequestsText(models.Model):
    name = models.TextField()
    value = models.TextField()
    customMember_service_request = models.ForeignKey(Rel8CustomMemberServiceRequests,on_delete=models.CASCADE)
class Rel8CustomMemberServiceRequestTextFile(models.Model):
    name = models.TextField()
    value = models.FileField(upload_to='servicerequestfile/%d/',
        storage=RawMediaCloudinaryStorage(),
                             )
    customMember_service_request = models.ForeignKey(Rel8CustomMemberServiceRequests,on_delete=models.CASCADE)
