import logging
import os
from bs4 import BeautifulSoup

def parseFile(f):
    print(f)
    soup = BeautifulSoup(f, features="xml")
    kanji = soup.find("keb")
    xref  = soup.find_all("xref")
    reb   = soup.find_all("reb")
    gloss = soup.find_all("gloss")
    print(kanji)
    print(xref)
    print(reb)
    print(gloss)

def parseSmallFiles():
    for root, dirs, files in os.walk("tmp"):
        for File in files:
            parseFile(File)
            break

def populateDatabase():
    if not os.path.exists(os.getcwd() + os.path.sep + "tmp"):
        os.system('python small_parser.py')

    parseSmallFiles()

populateDatabase()
