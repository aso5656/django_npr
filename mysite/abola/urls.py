from django.urls import path
from .views import *

app_name = 'abola'

urlpatterns = [
    path('',index, name='index'),
    path('<str:team>',render_team,name='render_team'),
]