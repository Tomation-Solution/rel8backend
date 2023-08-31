
from novu.config import NovuConfig
from novu.api.subscriber import SubscriberApi
from novu.dto.subscriber import SubscriberDto
from novu.api import EventApi
import os,json
from django.utils.text import slugify
from novu.api import TopicApi
from novu.api import EventApi
from novu.dto.topic import TriggerTopicDto
from django.db import models, connection





class NovuProvider:

    def __init__(self) -> None:
        self.api_key= os.environ.get('YOUR_NOVU_API_KEY')

    def connect(self):
        api_key= os.environ.get('YOUR_NOVU_API_KEY')
        n =NovuConfig().configure("https://api.novu.co", api_key)

    def subscribe(self,userID:int,email:str,):
        api_key= os.environ.get('YOUR_NOVU_API_KEY')
        NovuConfig().configure("https://api.novu.co", api_key)
        subscriber = SubscriberDto(
        subscriber_id=f'{userID}-{connection.schema_name}',
        email=email,)
        SubscriberApi().create(subscriber)

    def send_notification(self,name:str,sub_id,title,content):
        api_key= os.environ.get('YOUR_NOVU_API_KEY')
        n =NovuConfig().configure("https://api.novu.co", api_key)

        clean_sub_id = list(map(lambda x:f'{x}-{connection.schema_name}',sub_id))
        print({
            'sub':clean_sub_id
        })
        EventApi().trigger(
            name=name,  
            recipients=clean_sub_id,
            payload={"title":title,'content':content}
        )


    def create_topic(self,name):
        key = slugify(name)
        self.connect()
        TopicApi().create(key=key,name=name)

    def sub_user_to_topic(self,name,user_ids):
        self.connect()
        key = slugify(name)
        TopicApi().subscribe(key=key,
                subscribers=user_ids)
        
    def notify_by_topic(self,topicName,title,content,workflowName='on-boarding-notification'):
        self.connect()
        topics = TriggerTopicDto(
        topic_key=slugify(topicName),
        type="Topic",
        )
        print({
            'topic':slugify(topicName),
            'workflow':workflowName
        })
        EventApi().trigger_topic(
        name=workflowName,  # The trigger ID of the workflow. It can be found on the workflow page.
        topics=topics,
        payload={"title":title,'content':content})