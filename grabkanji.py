# Script to download all kanji from yarxi.ru dictionary
import http.client
from urllib.parse import urlencode
import time

headers = {
  "Content-type": "application/x-www-form-urlencoded",
  "Accept": "text/html",
  "Accept-Language":"en-US,en",
  "Host": "yarxi.ru",
  "Connection": "Keep-Alive",
  "Origin": "http://yarxi.ru",
  "Referer": "http://yarxi.ru/",
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)",
  "X-Requested-With": "XMLHttpRequest"
}

params = {
    "N": 234
}

params = urlencode(params)

#"/search.php"

words = "/tref.php?N={}&ID="

entry_number_start = 6400
entry_number_end   = entry_number_start + 100
file_name = 'kanjidb{}_{}.html'.format(entry_number_start, entry_number_end-1)

conn = http.client.HTTPConnection("yarxi.ru")

with open(file_name, mode='w', encoding='utf8') as result_file:
    for number in range(entry_number_start, entry_number_end):
        conn.request("GET", "/entry.php?N={}".format(number), params, headers)
        r1 = conn.getresponse()
        if 100 <= r1.status < 400:
            print(' {} ok'.format(number))
            text = r1.read().decode('utf-8', "replace")
            result_file.write(text)
            result_file.write('<hr>\n')
        else:
            print('Error result {} for kanji {}'.format(r1.status, number))
        time.sleep(0.5)
conn.close()

