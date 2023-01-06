from django.contrib import admin
from . import models
# Register your models here.




# admin.site.register(models.News)


class  ParagraphAdmin(admin.TabularInline):
    model = models.NewsParagraph
    extra: int=0

class NewsAdmin(admin.ModelAdmin):
   inlines = [ParagraphAdmin,]

admin.site.register(models.News,NewsAdmin)