import requests
import re
from bs4 import BeautifulSoup

import threading

downloadSem = threading.Semaphore(10)
mutex = threading.Lock()

link = "http://www.manythings.org/kanji/d/index{}.html"
klink = "http://www.manythings.org/kanji/d/"
pages = ["", "2", "3", "4", "5"]

kanji = []

data = open("data.csv", "w")
data.write("id,kanji,tran\n")

headers = {'Host': 'www.manythings.org', 'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'DNT': '1', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

def parseKanji(l, k, i):
    downloadSem.acquire()
    page = requests.get(klink + l, headers=headers)
    downloadSem.release()

    page.encoding = 'shift-jis'
    page_text = page.text
    translateRE = re.compile(r'<h1>(.+?)</h1><font size=4>(.+?)</font>')
    try:
        translation = translateRE.search(page_text).group(2)
        #translation = re.sub(r',', '', translation)
    except AttributeError:
        return

    print(translation)

    mutex.acquire()
    data.write(str(i) + ',' + k + ',' + translation + '\n')
    mutex.release()

def parsePage(page):
    global kanji

    page = requests.get(link.format(page), headers=headers, stream=True)
    page.encoding = 'shift-jis'
    #page_text = page.raw.read()
    page_text = page.text
    print(type(page_text))
    print(page_text)

    kanjiRE = re.compile(r'<A HREF="(.+?)">(.+?)</a>')
    matches = kanjiRE.finditer(page_text)
    for match in matches:
        l = match.group(1)
        k = match.group(2)
        kanji.append((l, k))
    #print(page_text.decode('utf-8', errors='replace'))
    pass

for page in pages:
    parsePage(page)

threads = []

for i, k in enumerate(kanji):
    t = threading.Thread(target=parseKanji, args=(k[0], k[1], i))
    t.start()
    threads.append(t)

    #parseKanji(k[0], k[1], i)
#page = requests.get('http://www.manythings.org/kanji/d/4e00.htm', headers=headers)
#page.encoding = 'shift-jis'
#page = page.text
#print(page)

for t in threads:
    t.join()

data.close()

#for i in kanji:
    #print(i[0] + " " + str(i[1].encode('utf-8')))
