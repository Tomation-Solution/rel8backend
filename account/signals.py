from account.models.user import User,ExcoRole,CommiteeGroup
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from utils.unique_account_creation_key_generator import key_generator
# from mailing.tasks import send_activation_mail
from utils.notification import NovuProvider
from account.models.auth import Chapters






