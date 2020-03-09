import requests
import re
from bs4 import BeautifulSoup

link = "http://www.manythings.org/kanji/d/index{}.html"
klink = "http://www.manythings.org/kanji/d/"
pages = ["", "2", "3", "4", "5"]

kanji = []

data = open("data.csv", "w")
data.write("kanji,tran,count")

headers = {'Host': 'www.manythings.org', 'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'DNT': '1', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

def parseKanji(l, k):
    page = requests.get(klink + l, headers=headers)
    page.encoding = 'shift-jis'
    page_text = page.text
    translateRE = re.compile(r'<h1>(.+?)</h1><font size=4>(.+?)</font>')
    translation = translateRE.search(page_text).group(2)
    print(translation)
    data.write(k + ',' + translation + '\n')

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

for k in kanji:
    parseKanji(k[0], k[1])
#page = requests.get('http://www.manythings.org/kanji/d/4e00.htm', headers=headers)
#page.encoding = 'shift-jis'
#page = page.text
#print(page)
data.close()

#for i in kanji:
    #print(i[0] + " " + str(i[1].encode('utf-8')))
