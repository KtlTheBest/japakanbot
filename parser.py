# -*- coding: utf-8 -*-
import logging
import os
from bs4 import BeautifulSoup
import re
import dbhandler

def grabber(soup, tag):
    content = soup.find_all(tag)
    res = []
    for item in content:
        x = item.text
        res.append(x.encode('unicode-escape'))

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


def parseFile(folder, f):
    #print("Writing " + f + " to dictionary")
    with open(folder + os.path.sep + f) as File:
        content = File.readlines()
        content = "".join(content)
        print(content)

    try:
        soup  = BeautifulSoup(content, features="xml")
        kanji = grabber(soup, "keb")
        xref  = grabber(soup, "xref")
        reb   = grabber(soup, "reb")
        gloss = grabber(soup, "gloss")

        addEntries2DB(int(f), kanji, xref, reb, gloss)
    except:
        print("Some error with parsing file {}. Silently passing".format(f))
        pass

def parseSmallFiles():
    for root, dirs, files in os.walk("tmp"):
        for File in files:
            parseFile(root, File)

def populateDatabase():
    if not os.path.exists(os.getcwd() + os.path.sep + "tmp"):
        os.system('python small_parser.py')

    parseSmallFiles()

populateDatabase()
