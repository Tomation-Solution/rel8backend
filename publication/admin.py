from django.contrib import admin
from  . import models
# Register your models here.



class  ParagraphAdmin(admin.TabularInline):
    model = models.PublicationParagraph
    extra: int=0

class PublicationAdmin(admin.ModelAdmin):
   inlines = [ParagraphAdmin,]

admin.site.register(models.Publication,PublicationAdmin)