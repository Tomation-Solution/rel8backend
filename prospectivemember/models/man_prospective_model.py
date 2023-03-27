from django.db import models
from django.contrib.auth import get_user_model


class RegistrationAmountInfo(models.Model):
    "it will be only on instance that will ever exist"
    amount =  models.DecimalField(decimal_places=2,max_digits=10)

class ManProspectiveMemberProfile(models.Model):
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=600)
    telephone_number = models.CharField(max_length=600)
    cac_registration_number = models.TextField(max_length=600)
    email = models.EmailField()
    website =models.URLField()
    corporate_office_addresse = models.TextField()
    has_paid = models.BooleanField(default=False)
    paystack = models.CharField(max_length=300)
    amount =  models.DecimalField(decimal_places=2,max_digits=10,default=0.00)

    class ManProspectiveMemberApplicationStatusChoice(models.TextChoices):
        approval_in_progress = 'approval_in_progress'
        approval_in_principle_granted = 'approval_in_principle_granted'
        final_approval = 'final_approval'

    application_status = models.CharField(max_length=100,choices=ManProspectiveMemberApplicationStatusChoice.choices,default=ManProspectiveMemberApplicationStatusChoice.approval_in_progress)

    def __str__(self):
        return self.name_of_company




"only paid Prospective can do this"

class ManProspectiveMemberFormOne(models.Model):
    prospective_member = models.OneToOneField(ManProspectiveMemberProfile,on_delete=models.CASCADE)
    cac_registration_number = models.TextField(max_length=600)
    name_of_company = models.CharField(max_length=600)

    tax_identification_number = models.TextField()
    corporate_office_addresse = models.TextField()
    office_bus_stop = models.TextField()
    office_city = models.TextField()
    office_lga = models.TextField()
    office_state = models.CharField(max_length=300)
    postal_addresse = models.CharField(max_length=300)
    telephone = models.CharField(max_length=13)
    email_addresse = models.EmailField()
    website =models.URLField()

    factoru_details = models.TextField()
    legal_status_of_company = models.CharField(max_length=100)
    number_of_female_expatriates = models.IntegerField(default=0)
    number_of_male_expatriates = models.IntegerField(default=0)
    number_of_male_permanent_staff= models.IntegerField(default=0)
    number_of_female_permanent_staff= models.IntegerField(default=0)
    local_share_capital = models.TextField(default=".")
    foreign_share_capital = models.TextField(default=".")

    ownership_structure_equity_local = models.TextField(default=".")
    ownership_structure_equity_foregin = models.TextField(default=".")
    total_value_of_land_asset = models.TextField(default=".")
    total_value_of_building_asset = models.TextField(default=".")
    total_value_of_other_asset = models.TextField(default=".")
    installed_capacity = models.TextField(default=".")
    current_sales_turnover = models.TextField(default=".")
    projected_sales_turnover = models.TextField(default=".")
    are_your_product_exported = models.TextField(default=".")
    company_contact_infomation = models.TextField(default=".")
    designation = models.TextField(default=".")
    name_of_md_or_ceo_of_company = models.TextField(default=".")
    selectdate_of_registration = models.DateField(null=True,default=None)
    upload_signature = models.ImageField(upload_to='upload_signature/%m/',null=True,default=None)
    # {'product_manufactured':'whothey breat','certificates':'certifacet of thoe'}
    all_roduct_manufactured = models.JSONField(default=list)

    # {'major_raw_materials':'j frhufr','major_raw_materials':'hello people'}
    all_raw_materials_used = models.JSONField(default=list)
    def __str__(self):
        return f'form one {self.prospective_member.name_of_company}'

# class AllProductManufactured(models.Model):
#     man_prospective_member_form_one = models.ForeignKey(ManProspectiveMemberFormOne,on_delete=models.CASCADE)
#     product_manufactured = models.TextField()
#     certificates = models.TextField()

# class AllRawMaterialsUsed(models.Model):
#     man_prospective_member_form_one = models.ForeignKey(ManProspectiveMemberFormOne,on_delete=models.CASCADE)
#     major_raw_materials = models.TextField()
#     major_raw_materials = models.IntegerField()




class ManProspectiveMemberFormTwo(models.Model):
    corporate_affairs_commision = models.FileField(upload_to='corporate_affairs_commision/')
    letter_of_breakdown_of_payment_and_docs_attached = models.FileField(upload_to='letter_of_breakdown_of_payment_and_docs_attached/')
    first_year_of_buisness_plan = models.FileField(upload_to='first_year_of_buisness_plan/')
    second_year_of_buisness_plan = models.FileField(upload_to='second_year_of_buisness_plan/')
    photocopy_of_your_reciept_issued_on_purchase_of_applicant_form = models.FileField(upload_to='photocopy_of_your_reciept_issued_on_purchase_of_applicant_form/')
    prospective_member = models.OneToOneField(ManProspectiveMemberProfile,on_delete=models.CASCADE)

    def __str__(self):
        return f'form two {self.prospective_member.name_of_company}'
