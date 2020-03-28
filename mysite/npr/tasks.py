from __future__ import absolute_import, unicode_literals
from celery import task
from .models import Podcast,Episode
from django.template.defaultfilters import slugify
import grequests
import requests
from bs4 import BeautifulSoup


@task()
def task_number_one():

    pod_link_list = list(Podcast.objects.values_list('link',flat=True).order_by('p_id'))
    pod_id_list = list(Podcast.objects.values_list('p_id',flat=True).order_by('p_id'))

    pod_render_list = ['https://www.npr.org/get/{}/render/partial/next?start=1'.format(u.split("/")[-2]) for u in pod_link_list]

    req = (grequests.get(u) for u in pod_render_list)

    resp = grequests.map(req,size=len(pod_render_list))

    id_resp_zip = list(zip(pod_id_list,resp))

    all_episode_list = [resp_render(item) for item in id_resp_zip]

    for each_pod in all_episode_list:
        for ep in each_pod:
            check_ep_exist(ep)

    return None

def resp_render(zip_list):
    
    soup = BeautifulSoup(zip_list[1].content,'html.parser')

    list_ep = soup.select('.podcast-episode')

    episode_set = [get_ep(each,zip_list[0]) for each in list_ep]

    print(zip_list[0])
    return episode_set

def get_ep(each,p_id):
    episode = {}
    episode['p_id'] = p_id
    episode['title'] = each.select('.title')[0].text
    episode['time'] = each.select('.episode-date')[0].time.get('datetime')
    episode['teaser'] = each.select('.teaser')[0].text.strip()
    episode['slug'] = slugify(episode['time']+'-'+episode['title'])

    if each.select('.title')[0].find_all('a'):
        episode['link'] =each.select('.title')[0].a.get('href')
    else:
        episode['link'] ="#"


    if each.select('.audio-tool-download'):
        media_link = each.select('.audio-tool-download')[0].a.get('href')
        media_link = media_link[:media_link.find('.mp3')+4]
    else:
        media_link=""
    episode['media_link'] = media_link

    if each.select('.imagewrap'):
        episode['img_link'] = each.select('.imagewrap')[0].find_all('img')[0].get('src')
    else:
        episode['img_link'] = ""


    if each.select('.audio-tool-transcript'):
        episode['transcript_link'] =each.select('.audio-tool-transcript')[0].a.get('href')
    else:
        episode['transcript_link']=""
    
    return episode

def check_ep_exist(ep):

    ep_check = Episode.objects.all().filter(slug=ep['slug']) #check if the query exist ep with same slug

    if ep_check.exists():
        return 
    else: #if not exist,create an episode
        new_ep = Episode(title=ep['title'],p_id=ep['p_id'],time = ep['time'],teaser = ep['teaser'],img_link=ep['img_link'],transcript_link=ep['transcript_link'],media_link=ep['media_link'],slug = ep['slug'])
        new_ep.save()
        print(new_ep.slug)
        return
        


    

