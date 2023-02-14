
from celery.utils.log import get_task_logger
from rel8.celery import app
from django.contrib.auth import get_user_model
from Dueapp import models
from celery import shared_task
from account.models import user as user_related_models

logger = get_task_logger(__name__)


@app.task()
def create_due_job(due_id,chapterID=None):
    """
        we not nessary creating a new due we just using the info of the due to charge a user
    """
    logger.info(f'{due_id},{type(due_id) } from matthew  chapterID:{chapterID} ' )
    try:
        if chapterID:
            # get all users with the chapterID 
            users =get_user_model().objects.all().filter(
                user_type='members',chapter__id=chapterID)

        else:
            # else just get all users
            users =get_user_model().objects.all().filter(
            user_type='members',)

        due =models.Due.objects.get(id=due_id)
        for eachMember in users:
            # let set the members that are being Charge it is_financial=False
            'is_for_excos if it false that means we getting all users else if its for only excos'
            member = user_related_models.Memeber.objects.get(user=eachMember,)
            perform_operatioon = False
            if due.dues_for_membership_grade.member.filter(id=member.id):
                perform_operatioon=True
            else:
                "this person is not in the alumni year dont charge him"
                perform_operatioon=False

            logger.info(f'perform_operatioon: {perform_operatioon} on member that has id of {member.id}')
            if perform_operatioon:
                # if member.is_exco==due.is_for_excos:
                member.is_financial=False
                member.amount_owing=member.amount_owing- due.amount
                member.save()
                dueUser = models.Due_User.objects.create(
                    user = eachMember,
                    due=due,
                    amount = due.amount
                )
                dueUser.save()
            
    except models.Due.DoesNotExist:
        logger.info('hello the Due DOes not exist')
 
# @shared_task
def create_deactivating_user_model(id,chapterID=None):
    "this would create DeactivatingDue for each user so they can pay"
    # """
    #     we not nessary creating a new due we just using the info of the due to charge a user
    # """
    
    try:
        if chapterID:
            # get all users with the chapterID 
            users =get_user_model().objects.all().filter(
                user_type='members',chapter__id=chapterID)

        else:
            # else just get all users
            users =get_user_model().objects.all().filter(
            user_type='members',)
        deactivatingDue =models.DeactivatingDue.objects.get(id=id)
        for eachMember in users:
            member = user_related_models.Memeber.objects.get(user=eachMember)
            member.amount_owing=member.amount_owing-deactivatingDue.amount
            member.save()
            "we are creating"
            dueUser = models.DeactivatingDue_User.objects.create(
                user = eachMember,
                deactivatingdue=deactivatingDue,
                amount = deactivatingDue.amount
            )
            dueUser.save()
           
        logger.info('Created payment succesffully')
    except models.Due.DoesNotExist:
        logger.info('hello the Due DOes not exist')
    



@app.task()
def deactivating_due_job(deactivatingdueID,chapterID=None):
    "we look for all DeactivatingDue_User that has to do with DeactivatingDue check if they have paid else we going to deactivate that user "
    all_users_deactivating_dues = models.DeactivatingDue_User.objects.filter(deactivatingdue=deactivatingdueID)

    for user_deactivating_due in all_users_deactivating_dues:
        # set the payment to overdue
        if user_deactivating_due.is_paid==False:
            user_deactivating_due.is_overdue=True
            user_deactivating_due.save()
            # deactivate this user
            member = user_related_models.Memeber.objects.get(user=user_deactivating_due.user)
            member.is_financial=False#because it time for payment and the user is owing that why we tag it false
            member.save()
            currentUser = get_user_model().objects.get(id=user_deactivating_due.user.id)
            currentUser.is_active=False
            currentUser.save()