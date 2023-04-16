
from celery.utils.log import get_task_logger
from rel8.celery import app
from django.contrib.auth import get_user_model
from Dueapp import models
from celery import shared_task
from account.models import user as user_related_models
from django.db.models import Q

logger = get_task_logger(__name__)

@app.task()
def create_exco_due(due_id,exco_id):
        # users =get_user_model().objects.all().filter(
        # user_type='members',exci__id=exco_id)
        due =models.Due.objects.get(id=due_id)
        excoRole = user_related_models.ExcoRole.objects.get(id=exco_id)
        for member in excoRole.member.all():
            # let set the members that are being Charge it is_financial=False
            models.Due_User.objects.create(
                user =member.user,
                due = due,
                amount=due.amount,
                is_overdue=False
            )
            member.amount_owing = member.amount_owing - due.amount
            member.save()

def create_membership_due(due_id,membershipgrade_id):
    grade=user_related_models.MemberShipGrade.objects.get(id=membershipgrade_id)
    due =  models.Due.objects.get(id=due_id)

    for member in grade.member.all():
            models.Due_User.objects.create(
                user =member.user,
                due = due,
                amount=due.amount,
                is_overdue=False
            )
            member.amount_owing = member.amount_owing - due.amount
            member.save()

        

@app.task()
def create_due_job(due_id,chapterID=None):
    """
    this function create general dues
    """
    logger.info(f'{due_id},{type(due_id) } from matthew  chapterID:{chapterID} ' )
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
        models.Due_User.objects.create(
            user =member.user,
            due = due,
            amount=due.amount,
            is_overdue=False
        )
        member.amount_owing = member.amount_owing - due.amount
        member.save()

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
def deactivate_owing_members(id,chapterID=None):
    'get all due_users that are meant to pay the Due'
    due = models.Due.objects.get(id=id)
    all_due_user = models.Due_User.objects.all().filter(due=due)
    for each_user  in all_due_user:
        if each_user.is_paid ==False:
            each_user.is_overdue=True
            each_user.save()
            member = user_related_models.Memeber.objects.get(
                user=each_user.user)
            member.is_financial=False
            member.save()




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