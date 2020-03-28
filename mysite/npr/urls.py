from django.urls import path

from . import views

app_name = 'npr'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('<str:order>/',views.IndexView.as_view(),name='index_by_order'),
    path('search',views.search,name='search'),
    path('category/<slug:slug>',views.CategoryView.as_view(),name= 'by_category'),
    path('<slug:slug>',views.PodcastView.as_view(),name='podcast'),
    #path('podcast/<int:p_id>/<slug:slug>',views.update_episode,name='update_podcast'),
    path('podcast/<slug:slug>/<int:page>',views.PodcastView.as_view(),name='podcast_by_page'),
]