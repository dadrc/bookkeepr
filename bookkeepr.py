#!/usr/bin/env python3
import sqlite3
from os.path import expanduser


class DBItem(object):
    dbpath = expanduser('~/.bookkeepr/user.db')

    def __init__(self):
        self.con = sqlite3.connect(self.dbpath)
        self.c = self.con.cursor()

    def load(self, itemId):
        self.cr.execute(self.fromQuery, itemId)
        return self.c.fetchone()

    def save(self, query, data):
        self.c.execute(query, data)
        self.con.commit()
        return c.lastrowid


class Bill(DBItem):
    @classmethod
    def fromDB():
        raise NotImplemented

    @classmethod
    def fromData():
        raise NotImplemented


class Tag(DBItem):
    @classmethod
    def fromDB():
        raise NotImplemented

    @classmethod
    def fromData():
        raise NotImplemented


class User(DBItem):
    @classmethod
    def fromDB():
        raise NotImplemented

    @classmethod
    def fromData():
        raise NotImplemented


class Currency(DBItem):
    fromQuery = 'SELECT name, symbol FROM currencies WHERE cid = ?'
    toQuery = 'INSERT INTO currencies (cid, name, symbol) VALUES (?,?,?)'
    dbpath = expanduser('~/.bookkeepr/user.db')

    @classmethod
    def fromData(self, name, symbol, cid=None):
        this = Currency()
        this.name = name
        this.symbol = symbol
        this.cid = cid
        return this

    @classmethod
    def fromDB(self, itemId):
        this = Currency()
        (this.name, this.symbol) = super.load(this, itemId)
        this.cid = itemId
        return this

    def toDB(self):
        con = sqlite3.connect(self.dbpath)
        c = con.cursor()
        c.execute(self.toQuery, (self.cid, self.name, self.symbol))
        con.commit()
        con.close()
        return c.lastrowid

    def toDBtest(self):
        return super.save(self.toQuery, (self.cid, self.name, self.symbol))

    def toString(self):
        print('Currency {}, Symbol {}'.format(self.name, self.symbol))


if __name__ == '__main__':
    c = Currency.fromData('Euro', '€')
    c.toString()
    cid = c.toDB()
    print('New ID: {}'.format(cid))
