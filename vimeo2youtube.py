# -*- coding: utf-8 -*-
import vimeo_dl as vimeo
import sqlite3
import os

number_of_uploaded_videos = 0

def vimeo_download(url):
        video = vimeo.new(url) 
        best = video.getbest()
        best.download(filepath="/home/antunes/scripts/scripts-pessoais/na-youtube")
        
        conn = sqlite3.connect('/home/antunes/scripts/scripts-pessoais/na-youtube/videos.sqlite')
        c = conn.cursor()
        c.execute('UPDATE videos SET download = 1 WHERE vimeo="%s"' % url)
        conn.commit()
        conn.close()

# Get title video on database
#def video_info(url):
#    conn = sqlite3.connect('/home/antunes/scripts/scripts-pessoais/na-youtube/videos.sqlite')
#    print('select titulo from videos  where vimeo == "%s"' % url)
#    c = conn.cursor()
#    title = c.execute('select titulo from videos  where vimeo == "%s"' % url)
#    return(title)
#    conn.close()

def youtube_upload(title,url):
        cmd = 'python2 upload_video.py --file="{a}.mp4"  --title="{b}" --description="{a}"'.format(a=title,b=title[:100])
        print(cmd)
        if os.system(cmd) == True:
                # Atualiza DB
                print('escrever que video foi upado ')
                conn = sqlite3.connect('/home/antunes/scripts/scripts-pessoais/na-youtube/videos.sqlite')
                c = conn.cursor()
                c.execute('UPDATE videos SET upload = 1 WHERE vimeo="%s"' % url)
                conn.commit()
                conn.close()


# Consultar videos não upados
# Sintaxe de sqlite3 para buscar NULL
# select vimeo from videos where download is NULL ;
def check_videos_to_upload(amount):
        conn = sqlite3.connect('/home/antunes/scripts/scripts-pessoais/na-youtube/videos.sqlite')
        c = conn.cursor()
        c.execute('select vimeo from videos where download is NULL ;')
        if amount == 1:
                #print(c.fetchone()[0])
                return(c.fetchone()[0])
        else:
                for linha in c.fetchall():
                        print(linha)
        conn.close()


#def changetitle(word):
#    for letter in word:
#        if letter == "/":
#            word = word.replace(letter,"_")
#    return word

def vimeo2upload(url):
        global number_of_uploaded_videos
        video = vimeo.new(url)
        # print('inicio download')
        vimeo_download(url)
        # print('downdoad finalizado')
        #print(video_info(url) + '.mp4')
        #lol = 'lol'
        #print(os.path.exists('/etc/password.txt'))

        print('inicio upload')
        #youtube_upload(changetitle(video.title),url)
        youtube_upload(video.title,url)
        print('upload finalizado')
        #python2 upload_video.py --file=".mp4"  --title="" --description=""
        number_of_uploaded_videos += 1

menu = ''
while menu != 'q':
        print( '\n', number_of_uploaded_videos, ' uploaded videos')
        print ('\nWhat do you need?')
        print ('1 - list new videos')
        print ('2 - manual upload')
        print ('3 - upload the new video in the queue')
        menu = input ()
        if menu == '1':
                check_videos_to_upload('all')     
        elif menu == '2':
            url = input('Insira a URL do video: ')
            vimeo2upload(url)
        elif menu == '3':
            vimeo2upload(check_videos_to_upload(1))
        elif menu == 'q':
            quit()
        else:
                print ('Insert a valid option\n')
