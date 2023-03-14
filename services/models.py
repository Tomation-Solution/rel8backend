from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from account.models import user as account_models
# Create your models here.


class ReissuanceOfCertForm(models.Model):
    name_of_company = models.CharField(max_length=200)
    cac_reg_number = models.CharField(max_length=200)
    tax_identification_number = models.CharField(max_length=200)
    man_reg_number = models.CharField(max_length=200)
    company_official_email = models.CharField(max_length=200)
    company_official_website = models.CharField(max_length=200)
    
    
    corporate_addresse = models.CharField(max_length=200)
    # {other_locations:str[]}
    other_factory_location = models.JSONField(default=dict)

    # {products_manufactured:str[]}
    products_manufactured = models.JSONField(default=dict)

    # {list_of_imported_materials_used_in_production:str[]}
    list_of_imported_materials_used_in_production = models.JSONField(default=dict)

    # {list_of_local_materials_used_in_production:str[]}
    list_of_local_materials_used_in_production = models.JSONField(default=dict)

    managing_director_email = models.EmailField()
    managing_director_phone = models.CharField(max_length=200)


    chief_finance_officer_phone = models.CharField(max_length=200)
    chief_finance_officer_email = models.CharField(max_length=200)

    head_of_admin_phone = models.CharField(max_length=200)
    head_of_admin_email = models.CharField(max_length=200)

    head_of_corporate_affair_phone = models.CharField(max_length=200)
    head_of_corporate_affair_email = models.CharField(max_length=200)


    officer_handling_man_issues_in_your_company_phone = models.CharField(max_length=200)
    officer_handling_man_issues_in_your_company_email = models.CharField(max_length=200)

    # year_turn_over = models.ForeignKey(YearlyTurnOver,on_delete=models.CASCADE)


class YearlyTurnOver(models.Model):
    reissuance_of_cert_form = models.ForeignKey(ReissuanceOfCertForm,on_delete=models.CASCADE,null=True,default=None,blank=True)
    year = models.CharField(max_length=10)
    attachment = models.FileField(upload_to='attachment_finicial_statement/%d/',
        storage=RawMediaCloudinaryStorage(),
        )
class ServicesStatus(models.TextChoices):
    pending = 'pending'
    in_review = 'in_review'
    approved = 'approved'
    disapprove = 'disapprove'


class ReissuanceOfCertServices(models.Model):
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)
 
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)

    reissuance_of_cert_form = models.ForeignKey(ReissuanceOfCertForm,on_delete=models.CASCADE)

class LossOfCertificateServices(models.Model):
    # submit completed reissuance form -> pendng
    """
    #This Model should have a permission checker for
        payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
    """
    reissuance_of_cert_form = models.ForeignKey(ReissuanceOfCertForm,on_delete=models.CASCADE,null=True,default=None)

    #an affidavit from a court of competent jurisdiction supporting the loss of the certificate
    affidavit_from_court_of_loss_of_cert = models.FileField(upload_to='affidavit_from_court_of_loss_of_cert/',storage=RawMediaCloudinaryStorage(),)
    amount_to_be_paid = models.DecimalField(decimal_places=2,max_digits=10)
    year_one_audited_finacial_statements  = models.FileField(upload_to='year_one_audited_finacial_statements/%d/',storage=RawMediaCloudinaryStorage(),)
    year_two_audited_finacial_statements  = models.FileField(upload_to='year_one_audited_finacial_statements/%d/',storage=RawMediaCloudinaryStorage(),)
    certificate_of_incorporation = models.FileField(upload_to='certificate_of_incorporation/%d/',storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)
 
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)


class ChangeOfName(models.Model):
    # submit completed reissuance form -> pendng
    reissuance_of_cert_form = models.ForeignKey(ReissuanceOfCertForm,on_delete=models.CASCADE,null=True,default=None)
    """
    #This Model should have a permission checker for
        payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
    """
    original_membership_certificate = models.FileField(upload_to='original_membership_certificate/%d/',storage=RawMediaCloudinaryStorage())

    amount_to_be_paid = models.DecimalField(decimal_places=2,max_digits=10)
    year_one_audited_finacial_statements  = models.FileField(upload_to='year_one_audited_finacial_statements/%d/',storage=RawMediaCloudinaryStorage(),)
    year_two_audited_finacial_statements  = models.FileField(upload_to='year_one_audited_finacial_statements/%d/',storage=RawMediaCloudinaryStorage(),)
    certificate_of_incorporation = models.FileField(upload_to='certificate_of_incorporation/%d/',storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)

class MergerOfMemberCompanies(models.Model):
    """
    #This Model should have a permission checker for
        payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
    """
    # Submit a letter requesting for the merger of the companies under the membership of the Association, 
    letter_requesting_merger_of_companies =  models.FileField(upload_to='letter_requesting_merger_of_companies/%d/',storage=RawMediaCloudinaryStorage(),)
    most_recent_audited_finicial_statement= models.FileField(upload_to='most_recent_audited_finicial_statement/%d/',storage=RawMediaCloudinaryStorage(),)
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)

class AllMembershipCertificatesAboutConcernedCompany(models.Model):
    merger_of_member_companies = models.ForeignKey(MergerOfMemberCompanies,on_delete=models.CASCADE)
    name_of_certificates  = models.TextField()
    document  =  models.FileField(upload_to='all_membership_certificates_about_concerned_company/%d/',storage=RawMediaCloudinaryStorage(),)
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)

    def __str__ (self):return self.name_of_certificates


class DeactivationOfMembership(models.Model):
    """
    #This Model should have a permission checker for
    payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
    """
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)
    letter_requesting_deactivation = models.FileField(upload_to='letter_requesting_deactivation/%d/',storage=RawMediaCloudinaryStorage(),)
    original_membership_certificate = models.FileField(upload_to='original_membership_certificate/%d/',storage=RawMediaCloudinaryStorage(),)
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)



class ActivationOfDeactivatedMember(models.Model):
    """
    #This Model should have a permission checker for
    payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
    """
    submit_most_recent_audited_financial_statement =  models.FileField(upload_to='submit_most_recent_audited_financial_statement/%d/',storage=RawMediaCloudinaryStorage(),)
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)


class UpdateOnProductsManufactured(models.Model):
    """
    #This Model should have a permission checker for
    payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
    """
    most_recent_financial_statement =  models.FileField(upload_to='most_recent_financial_statement/%d/',storage=RawMediaCloudinaryStorage(),)
    # 7d.	a submitted product update inspection report from the Branch Executive Secretary to confirm the correctness of the information provided by the company.
    product_update_inspection_report =  models.FileField(upload_to='product_update_inspection_report/%d/',storage=RawMediaCloudinaryStorage(),)
    status = models.CharField(max_length=300,choices=ServicesStatus.choices,default=ServicesStatus.pending)
    member = models.ForeignKey(account_models.Memeber,null=True,default=None,blank=True,on_delete=models.SET_NULL)

# class UpdateOnFactoryLocation(models.Model):
#     """
#     #This Model should have a permission checker for
#     payment of all outstanding subscription(s) as advised on the latest demand notice (payment), 
#     """
#     submit_most_recent_audited_financial_statement =  models.FileField(upload_to='submit_most_recent_audited_financial_statement/%d/',storage=RawMediaCloudinaryStorage(),)

#     # d.	a submitted Factory inspection report from the Branch Executive Secretary to confirm the existence of the company operational base at the specified location.
#     product_update_inspection_report =  models.FileField(upload_to='product_update_inspection_report/%d/',storage=RawMediaCloudinaryStorage(),)