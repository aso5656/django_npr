from django.shortcuts import render

from .functions import *

results = None
# Create your views here.
def index(request):
    global results
    results = news_fetch()
    context={
        'results' : results
        }
    print(results)
    return render(request,'base1.html',context)

def render_team(request,team):
    for r in results:
        for k,v in r.items():
            if k == team:
                team_news = resp_render(r[team])
                break
    context={
        'team_news':team_news
    }
    print(team_news)
    return render(request,'base1.html',context)