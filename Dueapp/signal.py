from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import user as user_models
from .models import Due, Due_User,DeactivatingDue


@receiver(post_save, sender=Due)
def createJobforDue(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:#if a new record was created.
        instance.create_due_job()
# @receiver(post_save, sender=Due_User)
# def deduct_due_from_member_account(sender, **kwargs):
#     instance = kwargs['instance']
#     if kwargs['created']:#if a new record was created.
#         "if it for excos inly get the excos user else get the members"
#         if instance.due.is_for_excos:
#             memeber = user_models.Memeber.objects.get(user=instance.user.id,is_exco=instance.due.is_for_excos)
#         else:
#             memeber = user_models.Memeber.objects.get(user=instance.user.id,is_exco=False)
#         is_financial = False
#         memeber.amount_owing=memeber.amount_owing+instance.amount
#         memeber.save()


@receiver(post_save, sender=DeactivatingDue)
def deactivating_due_job(sender, **kwargs):
    deactivating_due = kwargs['instance']
    if kwargs['created']:#if a new record was created.
        deactivating_due.deactivating_due_job()

