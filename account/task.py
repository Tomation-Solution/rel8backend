from account.models.user import Memeber,UserMemberInfo
from django.db.models import Q
import requests
from django.contrib.auth import get_user_model
import random,string,json,os
from celery import shared_task


@shared_task
def regiter_user_to_chat(member_id,):
    'this creates users on the third party chat app'
    member  = Memeber.objects.get(id=member_id)
    memberInfo = UserMemberInfo.objects.filter(
    Q(name='Name') | Q(name='full_name') | Q(name='first')
    | Q(name='first name')| Q(name='surname')| Q(name='name'),
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