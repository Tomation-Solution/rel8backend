from django.db import models
from account.models import user as user_models

# Create your models here.



# - Shows Contestants Details/profiles
# - Shows roles of positions applied for
# - Shows Constestant Manifesto
# - shows Message to Electorate (30 sec Video/Banner)
# - shows number of members that have voted
# - User can vote
# Note: Election Portal should show contestants details, posts post constesting for, post roles, constestant manifesto,
# Contestants message to electorates & No of members voted,  
"""

Election Should have a name -> Role Name Peeps are contesting for

members can vote one Time to



Members ->
    members are allowed to vote for contestant
    members are allowed to vote once
Contestant->
     members contesting for a postion
Postion
Ballot Box 
"""

class BallotBox(models.Model):
    name = models.CharField(max_length=300,default="Election 1")
    role_name = models.CharField(max_length=300 ,default="Role OF What?")
    role_detail = models.TextField(default="")
    is_close = models.BooleanField(default=False)

    election_startDate=models.DateField(null=True,default=None)
    election_endDate=models.DateField(null=True,default=None)
    
    election_endTime=models.TimeField(null=True,default=None)
    election_startTIme=models.TimeField(null=True,default=None)

class Postions(models.Model):
    ballotbox  = models.ForeignKey(BallotBox,on_delete=models.CASCADE,null=True,default=None,blank=True,)
    members_that_has_cast_thier_vote = models.ManyToManyField(user_models.Memeber,)
    postion_name= models.CharField(max_length=90)
class Contestant(models.Model): 
    member =  models.ForeignKey(user_models.Memeber,on_delete=models.CASCADE,)
    amount_vote = models.IntegerField()
    youtubeVidLink = models.TextField()#this works as manifesto
    aspirantBio = models.JSONField(default=None,null=True)#this works as m anifesto
    upload_manifesto_docs = models.FileField(null=True,default=None)
    upload_manifesto_image = models.FileField(null=True,default=None)
    # this contestant will be running for this postion 
    postion  = models.ForeignKey(Postions,null=True,default=None,blank=True,on_delete=models.SET_NULL)
    


    # def __str__(self):
    #     return f'Member {self.member.id} conteting  for "{self.postion.postion_name}"'

