import logging
import xml.etree.ElementTree as ET

def parseJM():
    FILENAME = "JMdict_e"
    tree = ET.parse(FILENAME)
    root = tree.getroot()
    print(root.listall())

parseJM()
