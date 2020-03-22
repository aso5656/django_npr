from django.db import models
from datetime import date

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True,blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'

class Podcast(models.Model):
    p_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    link = models.CharField(max_length=1000, blank=True, null=True)
    img = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True)
    def __str__(self):
        return self.title
    
    #get latest episode date
    def latest_episode(self):
        if self.episode_set.all():
            return self.episode_set.all().order_by('-time')[0].time 
        else:
            return "-"
    def sort_latest_episode(self):
        if self.episode_set.all():
            return self.episode_set.all().order_by('-time')[0].time 
        else:
            return date(1900,1,1)
    
    latest_episode.short_description = 'Latest episode'
    class Meta:

        db_table = 'podcast'

class Episode(models.Model):
    e_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    p = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    time = models.DateField(blank=True, null=True)
    teaser = models.CharField(max_length=2000, blank=True, null=True)
    img_link = models.CharField(max_length=2000, blank=True, null=True)
    transcript_link = models.CharField(max_length=2000, blank=True, null=True)
    media_link = models.CharField(max_length=2000, blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True)
    def __str__(self):
        return self.title

    class Meta:
        
        db_table = 'episode'


