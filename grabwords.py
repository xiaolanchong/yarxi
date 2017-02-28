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

#params = urlencode(params)
params = {}

words_url = "/tref.php?N={}&ID="

entry_number_start = 97954 + 1
entry_number_end   = entry_number_start + 10000
file_name = 'dict_{}_{}.html'.format(entry_number_start, entry_number_end-1)

conn = http.client.HTTPConnection("yarxi.ru")

with open(file_name, mode='w', encoding='utf8') as result_file:
    for number in range(entry_number_start, entry_number_end):
        conn.request("GET", words_url.format(number), params, headers)
        r1 = conn.getresponse()
        if 100 <= r1.status < 400:
            print(' {} ok'.format(number))
            text = r1.read().decode(encoding='utf-8')
            result_file.write(text)
            result_file.write('<hr>\n')
        else:
            print('Error result {} for kanji {}'.format(r1.status, number))
        time.sleep(0.5)
conn.close()
