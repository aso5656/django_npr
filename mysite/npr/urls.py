from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'npr'

urlpatterns = [
    path('',cache_page(60*60*24*7)(views.IndexView.as_view()),name='index'),#cache 7 days
    path('<str:order>/',views.IndexView.as_view(),name='index_by_order'),
    path('search',views.search,name='search'),
    path('category/<slug:slug>',cache_page(60*60*24*7)(views.CategoryView.as_view()),name= 'by_category'), #cache 7 days
    path('<slug:slug>',cache_page(60*30)(views.PodcastView.as_view()),name='podcast'), #cache 30 mins
    #path('podcast/<int:p_id>/<slug:slug>',views.update_episode,name='update_podcast'),
    path('podcast/<slug:slug>/<int:page>',views.PodcastView.as_view(),name='podcast_by_page'),
]