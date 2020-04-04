from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
app_name = 'abola'

urlpatterns = [
    path('',cache_page(60*60*24*10)(index), name='index'),#cacge index page for 10 days
    path('<str:team>', cache_page(60*15)(render_team),name='render_team'),
]