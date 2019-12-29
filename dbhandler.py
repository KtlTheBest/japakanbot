import logging
import sqlite
import os
import random

def exists(path):
    return os.path.exists(path)

class DBHandler:
    def init(self):
        self.DB_NAME = "db.sqlite"
        self.conn = sqlite3.connect(self.DB_NAME)
        self.totalWordsCount = self.countTotalWords()

        self.POOL   = "pool"
        self.WORDS  = "dict"
        self.LEARNT = "passed"

    def createTables(self):
        stmt = "CREATE TABLE IF NOT EXISTS pool (id, INT, count, INT)"
        self.conn.execute(stmt)
        stmt = "CREATE TABLE IF NOT EXISTS passed (id, INT)"
        self.conn.execute(stmt)
        stmt = "CREATE TABLE IF NOT EXISTS dict (id, INT, kanji, TEXT, furi, TEXT, trans, TEXT)"
        self.conn.execute(stmt)

        self.conn.commit()

    def countTotalWords(self):
        stmt = "SELECT COUNT(*) FROM dict"
        res = self.conn.execute(stmt).fetchone()
        return res[0]

    def addDictionaryRow(self, uniqueId, kanji, furi, trans):
        stmt = "INSERT INTO dict (id, kanji, furi, trans) VALUES (?, ?, ?, ?)"
        self.conn.execute(stmt, (uniqueId, kanji, furi, trans))
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
        for uniqueId from uniqueIdList:
            self.conn.execute(stmt, (uniqueId, ))
            self.conn.commit()

    def getWellKnownWordsFromPool(self, counter):
        stmt = "SELECT id FROM pool WHERE count >= ?"
        cur = self.conn.execute(stmt, (counter, ))
        return cur.fetchall()

    def removeWellKnownWords(self, counter):
        lst = self.getWellKnownWords(counter)
        self.removeWordsFromPool(lst)
