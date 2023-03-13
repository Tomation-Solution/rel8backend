from rest_framework import serializers
from services import models


class MemberLossOfCertificateServicesSerializers(serializers.ModelSerializer):


    class Meta:
        model = models.LossOfCertificateServices
        fields = ['affidavit_from_court_of_loss_of_cert',
                 'amount_to_be_paid','year_one_audited_finacial_statements',
                 'year_two_audited_finacial_statements','certificate_of_incorporation','status','id']
        
class MemberChangeOfNameSerializers(serializers.ModelSerializer):

    class Meta:
        model =models.ChangeOfName
        fields = (
            'original_membership_certificate',
            'amount_to_be_paid',
            'year_one_audited_finacial_statements',
            'year_two_audited_finacial_statements',
            'certificate_of_incorporation',
            'status','member','id'
        )
        read_only_fields=['status','member']

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

    class Meta:
        model = models.DeactivationOfMembership
        fields = (
            'letter_requesting_deactivation',
            'original_membership_certificate',
          'status','member','id'
        )
        read_only_fields=['status','member']

class MemberActivationOfDeactivatedMemberSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = models.ActivationOfDeactivatedMember
        fields= (
            'submit_most_recent_audited_financial_statement','id'
        )

class UpdateOnProductsManufacturedSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.UpdateOnProductsManufactured
        fields= (
            'most_recent_financial_statement',
            'product_update_inspection_report',
           'status','member','id'
        )
        read_only_fields=['status','member']