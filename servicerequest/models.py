from django.db import models
from account.models.user import Memeber
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here.


class MemberOfReissuanceOfCertificate(models.Model):
    attach_membership_receipt= models.FileField(upload_to='attach_membership_receipt/%m/%d/',
                                                 storage=RawMediaCloudinaryStorage(),
                                                )
    note = models.TextField()
    member = models.ForeignKey(Memeber,on_delete=models.SET_NULL,default=None,null=True)


class ChangeOfName(models.Model):
    attach_membership_certificate= models.FileField(upload_to='attach_membership_certificate/%m/%d/',
                                                 storage=RawMediaCloudinaryStorage(),
                                                    )
    membership_due_receipt= models.FileField(upload_to='membership_due_receipt/%m/%d/',
                                                 storage=RawMediaCloudinaryStorage(), )
    # upload_financial_statement of last (2 years)
    upload_financial_statement = models.FileField(upload_to='upload_financial_statement/%m/%d/',
                                                 storage=RawMediaCloudinaryStorage(),
                                                  )
    upload_incorporation_certificate= models.FileField(upload_to='upload_incorporation_certificate/%m/%d/',
                                                 storage=RawMediaCloudinaryStorage(),
                                                       )
    member = models.ForeignKey(Memeber,on_delete=models.SET_NULL,default=None,null=True)


class MergerOfCompanies(models.Model):
    'Attach requirement for Merger of Companies'
    upload_request_letter= models.FileField(upload_to='upload_request_letter/%m/%d/',
                                                 storage=RawMediaCloudinaryStorage(),
                                            )
    submit_most_recent_financial_statement  = models.FileField(upload_to='submit_most_recent_financial_statement/%m/%d/',
                                                               storage=RawMediaCloudinaryStorage(),
                                                               )
    upload_dues_reciept= models.FileField(upload_to='Upload_dues_reciept/%m/%d/',
                                          storage=RawMediaCloudinaryStorage(),)
    upload_membership_cert_for_both_companies= models.FileField(upload_to='Upload_membership_cert_for_both_companies/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(Memeber,on_delete=models.SET_NULL,default=None,null=True)


class DeactivationOfMembership(models.Model):
    # Deactivation request( Letter)
    deactivation_request =  models.FileField(upload_to='deactivation_request/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    submit_most_recent_financial_statement   =  models.FileField(upload_to='submit_most_recent_financial_statement/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    upload_all_levy_recipt =  models.FileField(upload_to='upload_all_levy_recipt/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(Memeber,on_delete=models.SET_NULL,default=None,null=True)


class ProductManufacturingUpdate(models.Model):
    proceed_to_update_your_profile =  models.FileField(upload_to='proceed_to_update_your_profile/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    submit_most_recent_financial_statement   =  models.FileField(upload_to='submit_most_recent_financial_statement/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    upload_all_levy_recipt =  models.FileField(upload_to='upload_all_levy_recipt/%m/%d/', storage=RawMediaCloudinaryStorage(),)

    upload_Product_update_report  =  models.FileField(upload_to='upload_Product_update_report/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(Memeber,on_delete=models.SET_NULL,default=None,null=True)


class FactoryLocationUpdate(models.Model):
    proceed_to_update_your_profile =  models.FileField(upload_to='proceed_to_update_your_profile/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    submit_most_recent_financial_statement   =  models.FileField(upload_to='submit_most_recent_financial_statement/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    upload_dues_reciept= models.FileField(upload_to='Upload_dues_reciept/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    upload_factory_inspection_report  =  models.FileField(upload_to='upload_factory_inspection_report/%m/%d/', storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(Memeber,on_delete=models.SET_NULL,default=None,null=True)
    