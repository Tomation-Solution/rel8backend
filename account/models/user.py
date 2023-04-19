from email.policy import default
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from typing import Dict
from utils.custom_exceptions import CustomError
from . import auth as auth_related_models
from django.db import connection
from django.db.models import Q

class MyUserManager(BaseUserManager):
    "this class helps manage the Custom user Model"
    def create_user(self,email,user_type,
    password=None,) -> "User":
        if not password:
            raise ValueError("Password is missing")

        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        # if connection.schema_name=='public':
        # user.is_active =True
        user.user_type=user_type

        user.save(using=self._db)
        return user


    def create_superuser(self,email,password=None,**super_user):

        print(super_user)
        # if(not super_user.get("first_name")):
        #     raise ValueError("First Name is Missing")

        # if(not super_user.get("last_name")):
        #     raise ValueError("Last Name is Missing")
        user =self.create_user(email=email,password=password,user_type="super_admin")
        user.is_admin =True
        user.is_superuser=True
        user.is_staff =True
        user.user_type="super_admin"
        user.temp_password =password
        user.is_active=True
        user.save()
        # we would use the user to create a super_admin model
        SUPERADMIN = Super_admin.objects.create(
            user = user,
            first_name=super_user.get("first_name"," "),
            last_name=super_user.get("last_name"," ")
        )
        SUPERADMIN.save()
        return user
        

    def create_admin(self,email,password=None,**admin_user):

        chapter = admin_user.get('chapter',None)
        if (chapter is None): raise CustomError({'error':'a admin needs to belong to a chapter'})
        user =self.create_user(email=email,password=password,user_type='admin')
        # user.is_staff =True
        user.is_admin =True
        user.user_type="admin"
        user.chapter = chapter
        user.save()
        admin = Admin.objects.create(
        user = user,
        first_name=admin_user.get("first_name"," "),
        last_name=admin_user.get("last_name"," "),
        )
        admin.save()
        return user
        
        

class User(AbstractBaseUser,PermissionsMixin,):
    class UserType(models.TextChoices):
        admin = "admin"
        super_admin="super_admin"
        members = "members"
        prospective_members = "prospective_members"
    email = models.EmailField(unique=True)
    is_invited= models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    photo = models.ImageField(default=None,null=True,upload_to='user_image/%d/')
    is_member= models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_prospective_Member=  models.BooleanField(default=False)
    user_type = models.CharField(choices=UserType.choices,max_length=25)
    is_superuser = models.BooleanField(default=False)
    # any user that is in the app must belong to a distric 
    chapter = models.ForeignKey(auth_related_models.Chapters,on_delete=models.SET_NULL,null=True)
    # chapter = models.OneToOneField(auth_related_models.Chapters,on_delete=models.SET_NULL)
    # temp_password is use to save the owner password tempoary when he sign up but
    #  the moment he creates a alumni organization we would use his details to create an account in his alumni org and set him to super user
    temp_password = models.TextField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    'this is the external chat api cred we using'
    userSecret = models.TextField(default='')
    userName = models.TextField(default='')


    objects= MyUserManager()

    def __str__(self) -> str:
        return f'{self.email}'




class Admin(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)


    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Super_admin(models.Model):
    "this is the owner of the Alumni"
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250,default="")
    last_name = models.CharField(max_length=250,default="")


    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} {self.user.email}'


class Memeber(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    amount_owing = models.DecimalField(decimal_places=4,max_digits=19,default=0.00)
    is_exco= models.BooleanField(default=False)
    # ones this person miss out on payment he doent become a finicial user
    is_financial = models.BooleanField(default=True)
    alumni_year= models.DateField()
    telephone_number = models.CharField(max_length=15,default='')
    address = models.TextField(default='')
    dob   = models.DateField(blank=True,null=True,default=None)
    citizenship    = models.CharField(default='',max_length=24)

# filter(
# )
    @property
    def full_name(self,):
        possible_name_outcomes = self.usermemberinfo_set.filter(
            Q(name='Name')|Q(name='NAMES') | 
            Q(name='names')|
            Q(name='full_name') | Q(name='first') | Q(name='first name')| Q(name='surname')| Q(name='name'))
        if len(possible_name_outcomes) == 0:
            return self.user.email
        name = possible_name_outcomes.first()
        return name.value

    @property
    def member_education(self):
        return self.membereducation_set.all()
    @property
    def member_employment_history(self):
        return self.memberemploymenthistory_set.all()

class MemberEducation(models.Model):
    member = models.ForeignKey(Memeber,on_delete=models.CASCADE)
    name_of_institution = models.TextField(default='')
    major = models.TextField(default='')
    degree = models.CharField(max_length=50,default='')
    language = models.CharField(max_length=50,default='')
    reading = models.CharField(max_length=50,default='')
    speaking = models.CharField(max_length=50,default='')
    date   = models.DateField(blank=True,null=True,default=None)
class MemberEmploymentHistory(models.Model):
    member = models.ForeignKey(Memeber,on_delete=models.CASCADE,null=True,default=None)
    postion_title = models.CharField(max_length=200)
    employment_from = models.DateField(blank=True,null=True,default=None)
    employment_to = models.DateField(blank=True,null=True,default=None)
    employer_name_and_addresse = models.CharField(max_length=200)
    
    # def __str__(self) -> str:
    #     return f'{self.first_name} {self.last_name}'

    # def __str__(self):
    #     return self
class UserMemberInfo(models.Model):
    "after the user passes the quetion in the excel uploaded by the aadmin we would fill all the info in the model name and value"
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250,null=True)
    member = models.ForeignKey(Memeber,on_delete=models.CASCADE)


class ExcoRole(models.Model):
    member = models.ManyToManyField(Memeber,) 
    name = models.CharField(max_length=500)
    about = models.TextField(default=' ')
    can_upload_min= models.BooleanField(default=False)#this means "can upload minute & Report in the exco insights/archieve"
    "if the chapter is none this mean this is a global exco else if it tied to one chapter this means this exco is for only that chapter"
    chapter = models.ForeignKey(auth_related_models.Chapters,on_delete=models.SET_NULL,null=True,default=None,blank=True)

    def __str__(self):return self.name
class MemberShipGrade(models.Model):
    member = models.ManyToManyField(Memeber,default=None,blank=True,) 
    name = models.CharField(max_length=500)
    chapter = models.ForeignKey(auth_related_models.Chapters,on_delete=models.SET_NULL,null=True,default=None,blank=True)

    def __str__(self) -> str:return self.name
# class PreviousExcoRoles(models.Model):
#     member = models.OneToOneField(Memeber,on_delete=models.SET_NULL,null=True) #only one member can have a postion at time
#     name = models.CharField(max_length=500)
#     about = models.TextField(default=' ')
#     created_on=models.DateTimeField(auto_now_add=True)


class CommiteeGroup(models.Model):
    name = models.CharField(max_length=200,default="")
    members = models.ManyToManyField(Memeber)
    team_of_reference = models.FileField(upload_to=f'teamOfReference/%d/',null=True)
    commitee_todo = models.JSONField(null=True)
    commitee_duties =  models.JSONField(null=True,default=None)
    def __str__(self):return f"{self.name}"

# class CommiteeTodo(models.Model):
#     commiteegroup = models.ForeignKey(CommiteeGroup,on_delete=models.CASCADE)


class CommiteePostion(models.Model):
    commitee_group = models.ForeignKey(CommiteeGroup,on_delete=models.CASCADE)
    "we have to check it this members are in commitee group "
    member  = models.ForeignKey(Memeber,on_delete=models.SET_NULL,null=True)
    name_of_postion = models.CharField(max_length=200,unique=True)
    duties = models.JSONField()


    def __str__(self): return self.name_of_postion

    def save(self, *args,**kwargs) -> None:
        if not self.member is None:
            if not self.commitee_group.members.all().filter(id=self.member.id).exists():
                raise CustomError({"error":"THis Member is not part of Commitee"})
            
        return super().save( *args,**kwargs)





