from account.models.user import (Memeber,UserMemberInfo,ExcoRole,
CommiteeGroup ,User,MemberShipGrade
)
from django.db.models import Q
import requests
from django.contrib.auth import get_user_model
import random,string,json,os
from celery import shared_task
from Dueapp import models as due_models
from account.models import user as user_related_models
from django.db import connection
from django.template.loader import render_to_string
from account.models.user import Memeber
from mymailing.views import send_mail

def create_chat(names:list,group_name:str,headers:dict):
    body ={
    'usernames':names,
    'title':group_name,
    'is_direct_chat':False
    }
    url = 'https://api.chatengine.io/chats/'
    resp = requests.put(url,headers=headers,data=json.dumps(body))


@shared_task
def update_membership_grade_chat(membership_id:int):
    grade=MemberShipGrade.objects.get(id=membership_id)
    all_member = grade.member.all()
    # auth_member is a member that has the extarnal chat api key
    auth_member  = all_member.first()
    if len(auth_member.user.userSecret) == 0:
        auth_member = all_member.last()
            
    headers = {
    'PRIVATE-KEY':os.environ['chat_private'] ,
    'Project-ID':os.environ['chat_projectid'],
    'Content-Type' : 'application/json',
    'Accept': 'application/json',
    'User-Name':auth_member.user.userName,
    'User-Secret':auth_member.user.userSecret,
    }
    all_names = []

    for member in all_member:
         member_info = UserMemberInfo.objects.filter(
                  Q(name='Name')|Q(name='NAMES') | 
                  Q(name='names')|
                  Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'),member=member)
         info = member_info.first()
         if info is not None:
              all_names.append(info.value)
    create_chat(names=all_names,group_name=grade.name,headers=headers)

# @shared_task
# def update_general_chat_group():
#         all_member  = Memeber.objects.all()
#         first_member  = all_member.first()
#         headers = {
#         'PRIVATE-KEY':os.environ['chat_private'] ,
#         'Project-ID':os.environ['chat_projectid'],
#         'Content-Type' : 'application/json',
#         'Accept': 'application/json',
#         'User-Name':first_member.user.userName,
#         'User-Secret':first_member.user.userSecret,
#         }
#         names = UserMemberInfo.objects.filter(
#                               Q(name='Name')|Q(name='NAMES') | 
#                   Q(name='names')|
#                   Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'),
#         ).values_list('value')
#         body ={
#              'usernames':names,
#              'title':'General Chat',
#              'is_direct_chat':False
#         }
#         url = 'https://api.chatengine.io/chats/'
#         resp = requests.put(url,headers=headers,data=json.dumps(body))

@shared_task
def regiter_user_to_chat(member_id,):
    'this creates users on the third party chat app'
    member  = Memeber.objects.get(id=member_id)
    memberInfo = UserMemberInfo.objects.filter(
                Q(name='Name')|Q(name='NAMES') | 
                  Q(name='names')|
                  Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'),
        member=member
    ).first()
    
    password =  ''.join(random.choices(string.ascii_uppercase +string.digits, k=7))

    url ='https://api.chatengine.io/users/'
    body = {
        "username":memberInfo.value,
        "first_name": "..",
        "last_name": "...",
        "secret":str(password),
        "custom_json":json.dumps( {"is_member": True})
    }
    headers = {
            'PRIVATE-KEY':os.environ['chat_private'] ,
            'Content-Type' : 'application/json',
            'Accept': 'application/json',}
    resp = requests.post(url,headers=headers,data=json.dumps(body))
    if resp.status_code == 201:
        user = get_user_model().objects.get(id=member.user.id)
        user.userSecret=password
        user.userName=memberInfo.value
        user.save()
        update_general_chat_group.delay()


@shared_task
def update_general_chat_group():
        all_member  = Memeber.objects.all()
        first_member  = all_member.first()
        headers = {
        'PRIVATE-KEY':os.environ['chat_private'] ,
        'Project-ID':os.environ['chat_projectid'],
        'Content-Type' : 'application/json',
        'Accept': 'application/json',
        'User-Name':first_member.user.userName,
        'User-Secret':first_member.user.userSecret,
        }
        names = UserMemberInfo.objects.filter(
                Q(name='Name')|Q(name='NAMES') | 
                  Q(name='names')|
                  Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'),
        ).values('value')
        def clean(data):return data.get('value')
        body ={
             'usernames':list(map(clean,names)),
             'title':'General Chat',
             'is_direct_chat':False
        }

        url = 'https://api.chatengine.io/chats/'
        resp = requests.put(url,headers=headers,data=json.dumps(body))

@shared_task
def update_exco_chat(excoRole_id:int):
      exco_role = ExcoRole.objects.get(id=excoRole_id)
      all_members = exco_role.member.all()
      '''
      #the reason for the this firs member is to gain access to the chat app because any 
      member can create group we just doing it programtically'''  
      first_member  = all_members.first()
      headers = {
        'PRIVATE-KEY':os.environ['chat_private'] ,
        'Project-ID':os.environ['chat_projectid'],
        'Content-Type' : 'application/json',
        'Accept': 'application/json',
        'User-Name':first_member.user.userName,
        'User-Secret':first_member.user.userSecret,}
      all_names = []
      for member in all_members:
            
            member_info = UserMemberInfo.objects.filter(
                  Q(name='Name')|Q(name='NAMES') | 
                  Q(name='names')|
                  Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'),member=member)
            info = member_info.first()
            print({'info':info,'member':member})
            if info is not None:
                all_names.append(info.value)
      create_chat(names=all_names,group_name=exco_role.name,headers=headers)

@shared_task
def update_commitee_chat(commitee_id:int):
    commtee_group = CommiteeGroup.objects.get(id=commitee_id)
    all_members = commtee_group.members.all()
    first_member  = all_members.first()
    headers = {
        'PRIVATE-KEY':os.environ['chat_private'] ,
        'Project-ID':os.environ['chat_projectid'],
        'Content-Type' : 'application/json',
        'Accept': 'application/json',
        'User-Name':first_member.user.userName,
        'User-Secret':first_member.user.userSecret,}  
    all_names = []
    for member in all_members:
        member_info = UserMemberInfo.objects.filter(
                  Q(name='Name')|Q(name='NAMES') | 
                  Q(name='names')|
                  Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'),member=member)
        info = member_info.first()
        if info is not None:
             all_names.append(info.value)
    create_chat(names=all_names,
                group_name=commtee_group.name+'(CommiteeGroup)',headers=headers)



@shared_task
def charge_new_member_dues__fornimn(user_id:int):
     'This Charge Members on Manul Dues .. this does not work for ont nimn but for org that have membership_grade'
     all_mannual =  due_models.Due.objects.filter(is_on_create=True)
     user = User.objects.get(id=user_id)
     names = UserMemberInfo.objects.filter(Q(name='MEMBERSHIP_GRADE')|Q(name='MEMBERSHIP_GRADE'.lower()),
                                           member=user.memeber
                                           ).first()
     if names:
        'get the member grade and add this user to it'
        grade,_ =MemberShipGrade.objects.get_or_create(name=names.value)
        grade.member.add(user.memeber)
        grade.save()
        # update_membership_grade_chat.delay(grade.id)
        for due in all_mannual:
            if due.dues_for_membership_grade is  not None:
                if due.dues_for_membership_grade.name ==names.value:
                    due_models.Due_User.objects.get_or_create(
                        user=user,
                        due=due,
                        amount=due.amount,
                        item_code=due.item_code)
            else:
                 'this are dues that does not have membership grade and is_on_create'
                 due_models.Due_User.objects.get_or_create(
                        user=user,
                        due=due,
                        amount=due.amount,
                        item_code=due.item_code)



@shared_task
def group_MAN_subSector_and_sector(exco_name,member_id,type='sector',):
    try:
        member = user_related_models.Memeber.objects.get(id=member_id)
        exco,created = user_related_models.ExcoRole.objects.get_or_create(name=f'{exco_name} {type}')
        exco.member.add(member)
        exco.save()
        # exco
    except:pass

@shared_task()
def send_forgot_password_mail(email,link):
    'send forgot password notifcation'
    mail_subject =f'{connection.schema_name.upper()}Forgot Password'
    user = get_user_model().objects.get(email=email)
    memeber = Memeber.objects.get(user=user)
    # link = f'https://{connection.schema_name}.rel8membership.com/reset-password/'
    sender_name=f'{connection.schema_name.upper()} Membeership Forgot Password'
    domain_mail = os.environ['domain_mail']
    sender_email =domain_mail
    
    if connection.schema_name == 'nimn':
         link='https://members.nimn.com.ng/forgot-password/'
    if connection.schema_name =='test':
         link = 'https://test.rel8membership.com/forgot-password/'
         
    data = {
         'link':link,
         'name':memeber.full_name
    }
    html_content = render_to_string('forgot_password.html',context=data)

    send_mail(
        subject=mail_subject,
        html_content=html_content,
        to=[{"email":email,"name":"rel8"}],
        sender={"name":sender_name,"email":sender_email})