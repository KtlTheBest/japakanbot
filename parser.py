# -*- coding: utf-8 -*-
import logging
import os
from bs4 import BeautifulSoup
import re
import dbhandler

def grabber(soup, tag):
    contentRE = re.compile(r'<(?P<tagField>.*?)(\s+?.*?)?>(.+?)</(?P=tagField)>')
    content = soup.find_all(tag)
    res = []
    for item in content:
        item = str(item)
        x = contentRE.search(item).group(3)
        res.append(x.decode('utf-8'))

    if len(res) == 0:
        res.append("")

    return res

def addEntries2DB(uniqueId, kanji, xref, reb, gloss):
    handler = dbhandler.DBHandler()

    for k in kanji:
        for x in xref:
            for r in reb:
                for g in gloss:
                    handler.addDictionaryRow(uniqueId, k, x, r, g)

    print("Added " + str(uniqueId) + " to dictionary")

def parseFile(folder, f):
    with open(folder + os.path.sep + f) as File:
        content = File.readlines()
        content = "".join(content)
    soup = BeautifulSoup(content, features="xml")
    kanji = grabber(soup, "keb")
    xref  = grabber(soup, "xref")
    reb   = grabber(soup, "reb")
    gloss = grabber(soup, "gloss")

    addEntries2DB(int(f), kanji, xref, reb, gloss)

def parseSmallFiles():
    for root, dirs, files in os.walk("tmp"):
        for File in files:
            parseFile(root, File)

def populateDatabase():
    if not os.path.exists(os.getcwd() + os.path.sep + "tmp"):
        os.system('python small_parser.py')

    parseSmallFiles()

populateDatabase()
