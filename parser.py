# -*- coding: utf-8 -*-
import logging
import os
from bs4 import BeautifulSoup
import re
import dbhandler

def grabber(soup, tag):
    contentRE = re.compile(r'<(?P<tagField>.*?)>(.+?)</(?P=tagField)>')
    content = soup.find_all(tag)
    res = []
    for item in content:
        item = str(item)
        x = contentRE.search(item).group(2)
        res.append(x.decode('utf-8'))

    if len(res) == 0:
        res.append("")

    return res

def addEntries2DB(kanji, xref, reb, gloss):
    handler = dbhandler.DBHandler()

    for k in kanji:
        for x in xref:
            for r in reb:
                for g in gloss:
                    handler.addDictionaryRow(k, x, r, g)

    res = handler.getDictContents()
    for row in res:
        print(row)

def parseFile(f):
    print(f)
    with open(f) as File:
        content = File.readlines()
        content = "".join(content)
    soup = BeautifulSoup(content, features="xml")
    kanji = grabber(soup, "keb")
    xref  = grabber(soup, "xref")
    reb   = grabber(soup, "reb")
    gloss = grabber(soup, "gloss")

    addEntries2DB(kanji, xref, reb, gloss)

def parseSmallFiles():
    for root, dirs, files in os.walk("tmp"):
        for File in files:
            parseFile(root + os.path.sep + File)

def populateDatabase():
    if not os.path.exists(os.getcwd() + os.path.sep + "tmp"):
        os.system('python small_parser.py')

    parseSmallFiles()

populateDatabase()
