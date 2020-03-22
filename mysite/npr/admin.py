from django.contrib import admin

# Register your models here.
from .models import *
class EpisodeInline(admin.StackedInline):
    model = Episode

class PodcastAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Category', {'fields': ['category'], 'classes': ['collapse']}),
        ('Description',{'fields':['description']})
    ]

    inlines = [EpisodeInline]
    list_display = ('title', 'category','latest_episode')
    list_filter = ['category']

admin.site.register(Podcast,PodcastAdmin)