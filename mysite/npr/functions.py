import requests
from bs4 import  BeautifulSoup
from django.template.defaultfilters import slugify
        

class UpdateEpisode(object):
    
    def __init__(self,pod_link,pod_id):
        self.podcast_link = pod_link
        self.podcast_id = pod_id
    

    def get_soup(self,url):
        header={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        
        requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        s = requests.session()
        s.keep_alive = False # 关闭多余连接
        res = s.get(url,headers=header)
        soup = BeautifulSoup(res.content,'html.parser')
        return soup

    def get_ep(self,each):
        
        
        episode = {}
        episode['p_id'] = self.podcast_id
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
            

    def render_episode(self):
        url_episode_render = 'https://www.npr.org/get/{}/render/partial/next?start={}'
        #remaining_count = 'https://www.npr.org/get/{}/remainingCount?start={}'
        podcast_number = self.podcast_link.split("/")[-2]
        
        start_position = 1

        #remaining_in_page = int(requests.get(remaining_count.format(podcast_number,start_position)).text)
        
        soup = self.get_soup(url_episode_render.format(podcast_number,start_position))

        #soup = get_soup(url_episode_render.format(podcast_number,start_position))
        list_ep = soup.select('.podcast-episode')

        episode_set = [self.get_ep(i) for i in list_ep]
        
        return episode_set
        


        