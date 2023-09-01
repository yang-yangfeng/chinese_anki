#!/usr/bin/python3
# vocab HSK anki
# pipeline to make my own hsk anki cards

import pymysql
import GoogleTTS

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
            GoogleTTS.audio_extract(input_text=row.simplified, args = {'language':'zh-CN','output':'audio/' + str(row.id) + '.mp3'})
finally:
    conn.close()


# write csv for anki import https://docs.ankiweb.net/importing/text-files.html, https://docs.ankiweb.net/importing/text-files.html#importing-media, https://superuser.com/questions/698902/can-i-create-an-anki-deck-from-a-csv-file

# import to anki