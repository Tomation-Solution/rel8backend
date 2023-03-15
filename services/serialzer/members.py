from rest_framework import serializers
from services import models

def seprateReissuanceCertToADict(validated_data:dict)-> dict:
    return {
            'name_of_company':validated_data.pop('name_of_company'),
            'cac_reg_number':validated_data.pop('cac_reg_number'),
            'tax_identification_number':validated_data.pop('tax_identification_number'),
            'man_reg_number':validated_data.pop('man_reg_number'),
            'company_official_email':validated_data.pop('company_official_email'),
            'company_official_website':validated_data.pop('company_official_website'),
            'corporate_addresse':validated_data.pop('corporate_addresse'),
            'other_factory_location':validated_data.pop('other_factory_location'),
            'products_manufactured':validated_data.pop('products_manufactured'),
            'list_of_imported_materials_used_in_production':validated_data.pop('list_of_imported_materials_used_in_production'),
            'list_of_local_materials_used_in_production':validated_data.pop('list_of_local_materials_used_in_production'),
            'managing_director_email':validated_data.pop('managing_director_email'),
            'managing_director_phone':validated_data.pop('managing_director_phone'),
            'chief_finance_officer_phone':validated_data.pop('chief_finance_officer_phone'),
            'chief_finance_officer_email':validated_data.pop('chief_finance_officer_email'),
            'head_of_admin_phone':validated_data.pop('head_of_admin_phone'),
            'head_of_admin_email':validated_data.pop('head_of_admin_email'),
            'head_of_corporate_affair_phone':validated_data.pop('head_of_corporate_affair_phone'),
            'head_of_corporate_affair_email':validated_data.pop('head_of_corporate_affair_email'),
            'officer_handling_man_issues_in_your_company_phone':validated_data.pop('officer_handling_man_issues_in_your_company_phone'),
            'officer_handling_man_issues_in_your_company_email':validated_data.pop('officer_handling_man_issues_in_your_company_email'),
            'year_turn_over_attachment':validated_data.pop('year_turn_over_attachment'),
        }

def _createReIssuanceForm(data,):
    'creates Reissuance of Cert Form'
    year_turn_over_attachment = data.pop('year_turn_over_attachment')
    reissuance_of_cert_form = models.ReissuanceOfCertForm.objects.create(
            **data
    )
    for turnoverData  in year_turn_over_attachment:
        models.YearlyTurnOver.objects.get_or_create(
            year =turnoverData.name ,
            attachment = turnoverData,
            reissuance_of_cert_form=reissuance_of_cert_form
        )
    return  reissuance_of_cert_form

# 
class ReissuanceOfCertCleaner(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    def get_member(self,instance):
        return {
            'full_name':instance.member.full_name,
            'id':instance.member.id,
        }
    class Meta:
        model = models.ReissuanceOfCertServices
        fields = '__all__'
        depth = 1
class ReissuanceOfCertSerializer(serializers.ModelSerializer):

    name_of_company = serializers.CharField()
    cac_reg_number = serializers.CharField()
    tax_identification_number = serializers.CharField()
    man_reg_number =serializers.CharField()
    company_official_email = serializers.CharField()
    company_official_website = serializers.CharField()
    
    
    corporate_addresse =serializers.CharField()
    # {other_locations:str[]}
    other_factory_location =serializers.ListField()

    # {products_manufactured:str[]}
    products_manufactured = serializers.ListField()

    # {list_of_imported_materials_used_in_production:str[]}
    list_of_imported_materials_used_in_production = serializers.ListField()

    # {list_of_local_materials_used_in_production:str[]}
    list_of_local_materials_used_in_production = serializers.ListField()

    managing_director_email =serializers.EmailField()
    managing_director_phone =  serializers.CharField()


    chief_finance_officer_phone =  serializers.CharField()
    chief_finance_officer_email =  serializers.CharField()

    head_of_admin_phone =  serializers.CharField()
    head_of_admin_email =  serializers.CharField()

    head_of_corporate_affair_phone =  serializers.CharField()
    head_of_corporate_affair_email =  serializers.EmailField()


    officer_handling_man_issues_in_your_company_phone =  serializers.CharField()
    officer_handling_man_issues_in_your_company_email = serializers.EmailField()
    year_turn_over_attachment = serializers.ListField(
        child= serializers.FileField(max_length=10000000,
        allow_empty_file=False,use_url=False,write_only=True))
    def create(self,validated_data):
        reissuance_of_cert_form = _createReIssuanceForm(validated_data)

        service = models.ReissuanceOfCertServices.objects.create(
            reissuance_of_cert_form=reissuance_of_cert_form,
            member= self.context.get('member')
        )
        return service

    class Meta:
        model = models.ReissuanceOfCertServices
        fields = '__all__'
        depth = 1


class MemberLossOfCeriticateServiceCleaner(serializers.ModelSerializer):
    yearly_turn_over = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_member(self,instance):
        return {
            'full_name':instance.member.full_name,
            'id':instance.member.id,
        }
    def get_yearly_turn_over(self,instance:models.LossOfCertificateServices):
        return models.YearlyTurnOver.objects.filter(reissuance_of_cert_form=instance.reissuance_of_cert_form.id).values(
            'year','attachment'
        )
        
    class Meta:
        model = models.LossOfCertificateServices
        # fields ='__all__'
        fields = ['affidavit_from_court_of_loss_of_cert','reissuance_of_cert_form','member',
        'amount_to_be_paid','year_one_audited_finacial_statements','yearly_turn_over',
        'year_two_audited_finacial_statements','certificate_of_incorporation','status','id','reissuance_of_cert_form']
        depth=1


class MemberLossOfCertificateServicesSerializers(serializers.ModelSerializer):

    name_of_company = serializers.CharField()
    cac_reg_number = serializers.CharField()
    tax_identification_number = serializers.CharField()
    man_reg_number =serializers.CharField()
    company_official_email = serializers.CharField()
    company_official_website = serializers.CharField()
    
    
    corporate_addresse =serializers.CharField()
    # {other_locations:str[]}
    other_factory_location =serializers.ListField()

    # {products_manufactured:str[]}
    products_manufactured = serializers.ListField()

    # {list_of_imported_materials_used_in_production:str[]}
    list_of_imported_materials_used_in_production = serializers.ListField()

    # {list_of_local_materials_used_in_production:str[]}
    list_of_local_materials_used_in_production = serializers.ListField()

    managing_director_email =serializers.EmailField()
    managing_director_phone =  serializers.CharField()


    chief_finance_officer_phone =  serializers.CharField()
    chief_finance_officer_email =  serializers.CharField()

    head_of_admin_phone =  serializers.CharField()
    head_of_admin_email =  serializers.CharField()

    head_of_corporate_affair_phone =  serializers.CharField()
    head_of_corporate_affair_email =  serializers.EmailField()


    officer_handling_man_issues_in_your_company_phone =  serializers.CharField()
    officer_handling_man_issues_in_your_company_email = serializers.EmailField()
    year_turn_over_attachment = serializers.ListField(
        child= serializers.FileField(max_length=10000000,
        allow_empty_file=False,use_url=False,write_only=True)
    )
    def create(self, validated_data):
        reissuanceOfCertDict = seprateReissuanceCertToADict(validated_data)
        reissuance_of_cert_form = _createReIssuanceForm(reissuanceOfCertDict)

        loss_of_certificate_services = models.LossOfCertificateServices.objects.create(
            **validated_data
        )
        loss_of_certificate_services.reissuance_of_cert_form=reissuance_of_cert_form
        loss_of_certificate_services.save()
        return loss_of_certificate_services

    class Meta:
        model = models.LossOfCertificateServices
        fields ='__all__'
        # fields = ['affidavit_from_court_of_loss_of_cert','reissuance_of_cert_form',
        #          'amount_to_be_paid','year_one_audited_finacial_statements',
        #          'year_two_audited_finacial_statements','certificate_of_incorporation','status','id']
        
class MemberChangeOfNameSerializers(serializers.ModelSerializer):
    name_of_company = serializers.CharField()
    cac_reg_number = serializers.CharField()
    tax_identification_number = serializers.CharField()
    man_reg_number =serializers.CharField()
    company_official_email = serializers.CharField()
    company_official_website = serializers.CharField()
    
    
    corporate_addresse =serializers.CharField()
    # {other_locations:str[]}
    other_factory_location =serializers.ListField()

    # {products_manufactured:str[]}
    products_manufactured = serializers.ListField()

    # {list_of_imported_materials_used_in_production:str[]}
    list_of_imported_materials_used_in_production = serializers.ListField()

    # {list_of_local_materials_used_in_production:str[]}
    list_of_local_materials_used_in_production = serializers.ListField()

    managing_director_email =serializers.EmailField()
    managing_director_phone =  serializers.CharField()


    chief_finance_officer_phone =  serializers.CharField()
    chief_finance_officer_email =  serializers.CharField()

    head_of_admin_phone =  serializers.CharField()
    head_of_admin_email =  serializers.CharField()

    head_of_corporate_affair_phone =  serializers.CharField()
    head_of_corporate_affair_email =  serializers.EmailField()


    officer_handling_man_issues_in_your_company_phone =  serializers.CharField()
    officer_handling_man_issues_in_your_company_email = serializers.EmailField()
    year_turn_over_attachment = serializers.ListField(
        child= serializers.FileField(max_length=10000000,
        allow_empty_file=False,use_url=False,write_only=True)
    )

    def create(self,validated_data):
        reissuanceOfCertDict = seprateReissuanceCertToADict(validated_data)
        reissuance_of_cert_form = _createReIssuanceForm(reissuanceOfCertDict)


        change_of_name  =models.ChangeOfName.objects.create(
            **validated_data
        )
        change_of_name.reissuance_of_cert_form=reissuance_of_cert_form
        change_of_name.save()
        return change_of_name
    class Meta:
        model =models.ChangeOfName
        # fields = (
        #     'original_membership_certificate',
        #     'amount_to_be_paid',
        #     'year_one_audited_finacial_statements',
        #     'year_two_audited_finacial_statements',
        #     'certificate_of_incorporation',
        #     'status','member','id'
        # )
        fields='__all__'
        read_only_fields=['status','member']
class MemberChangeOfNameCleaner(serializers.ModelSerializer):
    yearly_turn_over = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    def get_member(self,instance):
        return {
            'full_name':instance.member.full_name,
            'id':instance.member.id,
        }
    def get_yearly_turn_over(self,instance:models.ChangeOfName):
        try:
            return models.YearlyTurnOver.objects.filter(reissuance_of_cert_form=instance.reissuance_of_cert_form.id).values(
            'year','attachment'
        )
        except:return []
    class Meta:
        model = models.ChangeOfName
        fields = '__all__'
        depth = 1
        
class MemberAllMembershipCertificatesAboutConcernedCompanySerialzer(serializers.Serializer):
    name_of_certificates = serializers.CharField()
    merger_of_member_companies = serializers.CharField()
class MemberMergerOfMemberCompaniesSerializer(serializers.ModelSerializer):
    membership_cert_about_concerned_company = MemberAllMembershipCertificatesAboutConcernedCompanySerialzer(many=True,)


    def create(self, validated_data):
        letter_requesting_merger_of_companies = validated_data.get('letter_requesting_merger_of_companies')
        most_recent_audited_finicial_statement = validated_data.get('most_recent_audited_finicial_statement')

        merger_of_member_companies = models.MergerOfMemberCompanies(
            letter_requesting_merger_of_companies=letter_requesting_merger_of_companies,
            most_recent_audited_finicial_statement=most_recent_audited_finicial_statement
        )   

        # here we get all the membership_cert_about_concerned_company
        membership_cert_about_concerned_company= validated_data.get('membership_cert_about_concerned_company',[])

        for data in membership_cert_about_concerned_company:
            models.AllMembershipCertificatesAboutConcernedCompany.objects.create(
                merger_of_member_companies= merger_of_member_companies,


                name_of_certificates= data.get('name_of_certificates'),
                document= data.get('document'),
            )
        return  membership_cert_about_concerned_company

    class Meta:
        model = models.MergerOfMemberCompanies
        fields = (
            'letter_requesting_merger_of_companies',
            'most_recent_audited_finicial_statement',
            'status',
            'membership_cert_about_concerned_company','id'
        )


class MemberDeactivationOfMembershipSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    def get_member(self,instance):
        return {
            'full_name':instance.member.full_name,
            'id':instance.member.id,
        }
    class Meta:
        model = models.DeactivationOfMembership
        fields = (
            'letter_requesting_deactivation',
            'original_membership_certificate',
          'status','member','id'
        )
        read_only_fields=['status','member']

class MemberActivationOfDeactivatedMemberSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    def get_member(self,instance):
        return {
            'full_name':instance.member.full_name,
            'id':instance.member.id,
        }

    class Meta:
        model = models.ActivationOfDeactivatedMember
        fields= (
            'submit_most_recent_audited_financial_statement','id','member','status'
        )

class UpdateOnProductsManufacturedSerializer(serializers.ModelSerializer):

    member = serializers.SerializerMethodField()

    def get_member(self,instance):
        return {
            'full_name':instance.member.full_name,
            'id':instance.member.id,
        }
    class Meta:
        model = models.UpdateOnProductsManufactured
        fields= (
            'most_recent_financial_statement',
            'product_update_inspection_report',
           'status','member','id'
        )
        read_only_fields=['status','member']







# name_of_company= data.get('name_of_company'),    
# cac_reg_number= data.get('cac_reg_number'),    
# tax_identification_number= data.get('tax_identification_number'),    
# man_reg_number= data.get('man_reg_number'),    
# company_official_email= data.get('company_official_email'),    
# company_official_website= data.get('company_official_website'),    

# corporate_addresse= data.get('corporate_addresse'),    
# other_factory_location= data.get('other_factory_location'),    
# products_manufactured= data.get('products_manufactured'),    
# list_of_imported_materials_used_in_production= data.get('list_of_imported_materials_used_in_production'),    
# list_of_local_materials_used_in_production= data.get('list_of_local_materials_used_in_production'),    


# managing_director_email= data.get('managing_director_email'),    
# managing_director_phone= data.get('managing_director_phone'),    

# chief_finance_officer_phone= data.get('chief_finance_officer_phone'),    
# chief_finance_officer_email= data.get('chief_finance_officer_email'),    

# head_of_admin_phone= data.get('head_of_admin_phone'),    
# chief_finance_officer_email= data.get('chief_finance_officer_email'),    
