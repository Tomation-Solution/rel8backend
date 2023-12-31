# Generated by Django 3.2.13 on 2023-08-31 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_yearlyturnover_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allmembershipcertificatesaboutconcernedcompany',
            name='merger_of_member_companies',
        ),
        migrations.RemoveField(
            model_name='changeofname',
            name='member',
        ),
        migrations.RemoveField(
            model_name='changeofname',
            name='reissuance_of_cert_form',
        ),
        migrations.RemoveField(
            model_name='deactivationofmembership',
            name='member',
        ),
        migrations.RemoveField(
            model_name='lossofcertificateservices',
            name='member',
        ),
        migrations.RemoveField(
            model_name='lossofcertificateservices',
            name='reissuance_of_cert_form',
        ),
        migrations.RemoveField(
            model_name='mergerofmembercompanies',
            name='member',
        ),
        migrations.RemoveField(
            model_name='reissuanceofcertservices',
            name='member',
        ),
        migrations.RemoveField(
            model_name='reissuanceofcertservices',
            name='reissuance_of_cert_form',
        ),
        migrations.RemoveField(
            model_name='updateonproductsmanufactured',
            name='member',
        ),
        migrations.RemoveField(
            model_name='yearlyturnover',
            name='reissuance_of_cert_form',
        ),
        migrations.DeleteModel(
            name='ActivationOfDeactivatedMember',
        ),
        migrations.DeleteModel(
            name='AllMembershipCertificatesAboutConcernedCompany',
        ),
        migrations.DeleteModel(
            name='ChangeOfName',
        ),
        migrations.DeleteModel(
            name='DeactivationOfMembership',
        ),
        migrations.DeleteModel(
            name='LossOfCertificateServices',
        ),
        migrations.DeleteModel(
            name='MergerOfMemberCompanies',
        ),
        migrations.DeleteModel(
            name='ReissuanceOfCertForm',
        ),
        migrations.DeleteModel(
            name='ReissuanceOfCertServices',
        ),
        migrations.DeleteModel(
            name='UpdateOnProductsManufactured',
        ),
        migrations.DeleteModel(
            name='YearlyTurnOver',
        ),
    ]
