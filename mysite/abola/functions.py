import grequests
import requests
from bs4 import BeautifulSoup
from googletrans import Translator




def resp_render(url):
    res = requests.get(url)

    soup = BeautifulSoup(res.content,"html.parser")

    section1 = soup.select('.noticias')[0].find_all('a')
 
    news_links = ['https://www.abola.pt'+link.get('href') for link in section1]


    req = (grequests.get(u) for u in news_links)
    resp = grequests.map(req,size=len(news_links))

    
    news_list = [news_render(i) for i in resp] 

    return news_list

def news_render(res):

    soup = BeautifulSoup(res.content,"html.parser")
    
    translator = Translator()

    time_stamp = soup.select("#body_Ver_lblHora")[0].string
    
    title = soup.select("#body_Ver_lblTitulo")[0].string
    
    img = soup.select('#body_Ver_imgNoticia')
    
    if img:
        img = img[0].get('src')
    else:
        img = ''
        
    
    
    try:
    	title = translator.translate(title).text
    except:
    	title = title

    body = soup.select('#body_Ver_lblNoticia')[0].text
    news= {}
	
    news['title'] = title
    news['time_stamp']=time_stamp
    news['img'] = img
    
    
    try:
        body_trans = translator.translate(body).text
        news['body'] = body_trans
    except:
        news['body'] = body
    
    return news



    
def news_fetch():
    
    url = 'https://www.abola.pt/uc/Desporto/ListaClubes.aspx?e=7187'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    try:
        res = requests.get(url,headers=headers)

        soup = BeautifulSoup(res.content,"html.parser")
    except:

        club_links = [{'Wrong':'something wrong'}]
        return club_links
    else:

        club_ids = ['#rptClassificacaoPais_hplClubes_'+str(i) for i in range(0,18)]

        club_links = [{soup.select(i)[0].img.get('title').split('-')[0]:'https://www.abola.pt'+ soup.select(i)[0].get('href')} for i in club_ids]

        return club_links
