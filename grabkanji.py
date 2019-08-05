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
 # "Origin": "http://yarxi.ru",
 # "Referer": "http://yarxi.ru/",
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)",
  #"X-Requested-With": "XMLHttpRequest"
}

def dump_in_one_file(conn, file_name, entry_number_start, entry_number_end):
    with open(file_name, mode='w', encoding='utf8') as result_file:
        for number in range(entry_number_start, entry_number_end):
            conn.request("GET", "/entry.php?N={}".format(number), {}, headers)
            r1 = conn.getresponse()
            if 100 <= r1.status < 400:
                print(r1)
                print(' {} ok'.format(number))
                text = r1.read().decode('utf-8', "replace")
                result_file.write(text)
            else:
                r1.read()
                print('Error result {} for kanji {}'.format(r1.status, number))
            time.sleep(0.5)


def dump_in_multiple_files(conn, entry_number_start, entry_number_end):
    for entry_number in range(entry_number_start, entry_number_end):
        file_name = '{0:04}.html'.format(entry_number)
        with open(file_name, mode='w', encoding='utf8') as result_file:
            conn.request("GET", "/entry.php?N={}".format(entry_number), {}, headers)
            r1 = conn.getresponse()
            if 100 <= r1.status < 400:
                print(' {} ok'.format(entry_number))
                text = r1.read().decode('utf-8', "replace")
                result_file.write(text)
            else:
                print('Error result {} for kanji {}'.format(r1.status, entry_number))
            time.sleep(0.5)


entry_number_start = 6400
entry_number_end = entry_number_start + 300 + 1
single_file = False

conn = http.client.HTTPConnection("yarxi.ru")

if single_file:
    file_name = 'kanjidb{}_{}.html'.format(entry_number_start, entry_number_end - 1)
    dump_in_one_file(conn, file_name, entry_number_start, entry_number_end)
else:
    dump_in_multiple_files(conn, entry_number_start, entry_number_end)

conn.close()

