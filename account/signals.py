from account.models.user import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from mailing.models import EmailInvitation
from utils.unique_account_creation_key_generator import key_generator
from django.db import connection


@receiver(post_save,sender=User)
def send_confirmation_mail_to_user_after_save(sender,**kwargs):
    instance = kwargs['instance']
    print("Started" ,)
    print({'schema anme':connection.schema_name})
    if not connection.schema_name == 'public':
        if kwargs['created']  and not instance.is_active and not instance.is_superuser:
            email_activation_obj:EmailInvitation = EmailInvitation.objects.create(
                user=instance,
                email=instance.email
            )
            instance.is_registration_mail_sent = True
            instance.save()
            if not instance.is_invited:
                email_activation_obj.send_confirmation(first_name=" ", last_name="")



@receiver(post_save,sender=EmailInvitation)
def pre_save_email_activation(sender,**kwargs):
    instance = kwargs['instance']
    if not connection.schema_name == 'public':

        if not instance.activated and not instance.forced_expired:
            if not instance.key:
                instance.key = key_generator(instance)

                instance.save()