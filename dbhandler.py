import logging
import sqlite3
import os
import random

def exists(path):
    return os.path.exists(path)

class DBHandler:
    def __init__(self):
        self.DB_NAME = "db.sqlite"
        self.conn = sqlite3.connect(self.DB_NAME)
        try:
            self.totalWordsCount = self.countTotalWords()
        except sqlite3.OperationalError:
            self.totalWordsCount = 0

        self.POOL   = "pool"
        self.WORDS  = "dict"
        self.LEARNT = "passed"

        self.createTables()

    def dropTables(self):
        stmt = """
        DROP TABLE IF EXISTS pool;
        DROP TABLE IF EXISTS passed;
        DROP TABLE IF EXISTS dict;
        """

        self.conn.executescript(stmt)
        self.conn.commit()

    def createTables(self):
        stmt = """
        CREATE TABLE IF NOT EXISTS pool (id INT, count INT);
        CREATE TABLE IF NOT EXISTS passed (id INT);
        CREATE TABLE IF NOT EXISTS dict (id INTEGER PRIMARY KEY, kanji TEXT, xref TEXT, furi TEXT, trans TEXT);
        """

        self.conn.executescript(stmt)
        self.conn.commit()

    def countTotalWords(self):
        stmt = "SELECT COUNT(*) FROM dict"
        res = self.conn.execute(stmt).fetchone()
        return res[0]

    def getDictContents(self):
        stmt = "SELECT * FROM dict"
        res = self.conn.execute(stmt).fetchall()
        return res

    def addDictionaryRow(self, kanji, xref, furi, trans):
        stmt = "INSERT INTO dict (kanji, xref, furi, trans) VALUES (?, ?, ?, ?)"
        self.conn.execute(stmt, (kanji, xref, furi, trans))
        self.conn.commit()

    def getPassedWordsId(self):
        stmt = "SELECT * FROM passed"
        return self.conn.execute(stmt).fetchall()

    def chooseNRandomWords(self, count):
        lst = []
        passedWordsId = self.getPassedWordsId()

        for i in range(count):
            x = random.randint(1, self.totalWordsCount)
            while not (x in passedWordsId or x in lst):
                x = random.randint(1, self.totalWordsCount)
            lst.append(x)

        for x in lst:
            self.addWordPoolRow(x)

    def addWordPoolRow(self, uniqueId):
        stmt = "INSERT INTO pool (id, count) VALUES (?, ?)"
        self.conn.execute(stmt, (uniqueId, 0))
        self.conn.commit()

    def removeWordsFromPool(self, uniqueIdList):
        stmt = "DELETE FROM pool WHERE id=?"
        for uniqueId in uniqueIdList:
            self.conn.execute(stmt, (uniqueId, ))
            self.conn.commit()

    def getWellKnownWordsFromPool(self, counter):
        stmt = "SELECT id FROM pool WHERE count >= ?"
        cur = self.conn.execute(stmt, (counter, ))
        return cur.fetchall()

    def removeWellKnownWords(self, counter):
        lst = self.getWellKnownWords(counter)
        self.removeWordsFromPool(lst)
