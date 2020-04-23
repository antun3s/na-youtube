from bs4 import BeautifulSoup
from requests import get
import vimeo_dl as vimeo
import re
import sqlite3

def new_videos():
        site = 'https://www.noticiasagricolas.com.br'
        response = get('https://www.noticiasagricolas.com.br/videos/')
        html_soup = BeautifulSoup(response.text, 'html.parser')

        links = []

        for data in html_soup.find_all('div', class_='lista-wrapper middle'):
                for a in data.find_all('a'):
                        #print(site + a.get('href'))
                        links.append(site + a.get('href'))
        return(links)

def get_vimeo_url(url):
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        try:
                iframe = html_soup.iframe['src']
                if 'vimeo' in iframe:
                        iframe = re.sub('player\.|video/', "", iframe)
                        #iframe = re.sub('player.', "", iframe)
                        return(iframe)
        except:
                print('no video found')

def get_vimeo_title(url):
        video = vimeo.new(url)
        title = video.title.replace("'","").replace("/","-")
        print(title)
        return(title)

def insert_db(vimeo):
        conn = sqlite3.connect('/home/antunes/scripts/scripts-pessoais/na-youtube/videos.sqlite')
        c = conn.cursor()

        c.execute('SELECT * FROM videos WHERE vimeo= "%s"' % vimeo)
        entry = c.fetchone()
        
        if entry is None:
                c.execute("INSERT INTO videos (vimeo,titulo) VALUES ('%s','%s')" % (vimeo, get_vimeo_title(vimeo)))
                #print('New entry added')
        else:
                print('Entry found')

        conn.commit()
        conn.close()

videos = new_videos()
for video in videos:
        print(video)
        # Se nao retornar nada e meteorologia e nao armazena
        url = get_vimeo_url(video)
        if url != None:
                insert_db(url)

print('finalizado\n\n')