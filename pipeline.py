#!/usr/bin/python3
# vocab HSK anki
# pipeline to make my own hsk anki cards
import urllib
import urllib.request
import urllib.parse
import urllib.error
import time
import pymysql
import requests
from bs4 import BeautifulSoup
# import GoogleTTS

# create sql db of all HSK words with hanzi, pinyin, chinese from this: https://github.com/bachhuberdesign/chinese-vocabulary-database/blob/master/hsk-wordlist.sql
# DONE

# load db
conn = pymysql.connect(
    host='localhost',
    user='yangyangfeng',
    password='',
    db='hsk',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def save_byte_file(filename, content):
    with open(filename, "wb") as f:
        f.write(content)

# for each row in db
# get audio from google translate https://github.com/hungtruong/Google-Translate-TTS/blob/master/GoogleTTS.py
try:
    with conn.cursor() as cursor:
        # Read data from database
        sql = "SELECT * FROM vocabulary"
        cursor.execute(sql)

        # Fetch all rows
        rows = cursor.fetchall()

        # Print results
        for row in rows:
            # time.sleep(10)
            # GoogleTTS.audio_extract(input_text=row.get('simplified'), args = {'language':'zh-CN','output':'audio/' + str(row.get('id')) + '.mp3'})
            hanzi = row.get('simplified')
            row_id = row.get("id")

            # OLD CODE:
            # mp3url = 'https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=' + urllib.parse.quote(hanzi,encoding='UTF-8')
            # u2 = urllib.request.urlopen(mp3url)
            # mybytes = u2.read()
            # mystr = mybytes.decode("utf8")
            # u2.close()
            # soup = BeautifulSoup(mystr, 'html.parser')
            # alli = soup.find_all('i',class_='word_audio fa fa-volume-up')
            # audio_url = alli[0]['data-audio_url']
            # urllib.request.urlretrieve(audio_url,'audio/' + str(row.get('id')) + '.mp3')

            # Using: https://ttsmp3.com/text-to-speech/Chinese%20Mandarin/
            TTS_ENDPOINT = "https://ttsmp3.com/makemp3_new.php"
            payload = {
                "msg": hanzi,
                "lang": "Zhiyu",
                "source": "ttsmp3",
            }
            # Get MP3 file URL
            resp = requests.post(TTS_ENDPOINT, data=payload)
            
            # Check for erroneous response, raise exception
            if not resp.ok:
                raise Exception(f"API request error: {resp.status_code} ({resp.text})")
            mp3_url = resp.json()["URL"]
            # Download MP3 file data
            mp3_data_resp = requests.get(mp3_url)

            # Check for erroneous response, raise exception
            if not mp3_data_resp.ok:
                raise Exception(f"MP3 download request error: {mp3_data_resp.status_code} ({mp3_data_resp.text})")
            filename = f"{row_id}.mp3"
            save_byte_file(filename, mp3_data_resp.content)
            print(f"Saved `{hanzi}` as `{filename}`")

finally:    
    conn.close()


# write csv for anki import https://docs.ankiweb.net/importing/text-files.html, https://docs.ankiweb.net/importing/text-files.html#importing-media, https://superuser.com/questions/698902/can-i-create-an-anki-deck-from-a-csv-file

# import to anki