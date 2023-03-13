from django.db import models
from news import models as news_models
from publication import models as publication_models
class LastestUpdatesManager(models.Manager):

    def manage_publication(self,latest_publication:publication_models.Publication):
        publications = self.get_queryset().filter(latest_update_table_name='publication')
        if publications.exists():
            publications.delete()
        latest_publication_image =''
        try:lastest_news_image = latest_publication.image.url
        except:lastest_news_image=''

        self.create(
            latest_update_table_name='publication',
            latest_update_table_id = latest_publication.id,
            image_url_link = lastest_news_image,
            title = latest_publication.name,
            body = '....'+latest_publication.name
        )


    def manage_news(self,lastest_news:news_models.News):
        'helps create news as a latest update'
        news = self.get_queryset().filter(latest_update_table_name='news')
        if news.exists():
            news.delete()
        lastest_news_image = ''
        try:lastest_news_image = lastest_news.image.url
        except:lastest_news_image=''
        self.create(
            latest_update_table_name='news',
            latest_update_table_id = lastest_news.id,
            image_url_link=lastest_news_image,
            title = lastest_news.name,
            body = '......'+lastest_news.name
        )
    
class LastestUpdates(models.Model):
    """
        it will contain:
            1 - news
            1 - publication
            1 - event
            3 - birthdays
    """

    class TableLatestChoice(models.TextChoices):
        news='news' 
        birthday='birthday' 
        publication='publication' 
        event='event' 
    title = models.TextField()
    body = models.TextField()
    # image = models.ImageField(upload_to='latest_update/%d/',null=True,blank=True)
    image_url_link= models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)


    latest_update_table_id = models.IntegerField(null=True,default=None)
    latest_update_table_name = models.CharField(null=True,default=None,max_length=30)
    objects  = LastestUpdatesManager()

    def __str__(self):
        return self.title




