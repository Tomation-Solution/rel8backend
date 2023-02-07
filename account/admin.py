from django.contrib import admin
from .models import user,auth



admin.site.register(user.User)
admin.site.register(user.Super_admin)
admin.site.register(user.Admin)
admin.site.register(user.Memeber)
admin.site.register(user.UserMemberInfo)
admin.site.register(auth.SecondLevelDatabase)
admin.site.register(user.ExcoRole)
admin.site.register(user.MemberShipGrade)
admin.site.register(user.MemberEducation)
admin.site.register(user.MemberEmploymentHistory)



admin.site.register(user.CommiteeGroup)
admin.site.register(user.CommiteePostion)
admin.site.register(auth.Chapters)
# admin.site.register()