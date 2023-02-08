from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Gallery)
admin.site.register(models.Ticketing)



class  ImagesForGallery(admin.TabularInline):
    model = models.ImagesForGalleryV2
    extra: int=0

class GalleryV2Admin(admin.ModelAdmin):
   inlines = [ImagesForGallery,]

admin.site.register(models.GalleryV2,GalleryV2Admin)



admin.site.register(models.FundAProject)
admin.site.register(models.SupportProjectInCash)
admin.site.register(models.SupportProjectInKind)