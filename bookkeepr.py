#!/usr/bin/env python3
import sqlite3
from os.path import expanduser


class DBItem:
    fromQuery = ''
    toQuery = ''
    dbpath = expanduser('~/.bookkeepr/user.db')
    con = sqlite3.connect(dbpath)
    c = con.cursor()

    def load(self, itemId):
        self.cr.execute(self.fromQuery, itemId)
        return self.c.fetchone()

    def save(self, data, itemId=None):
        self.cursor.execute(self.toQuery, data.values)
        return self.c.lastrowid


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

    @classmethod
    def fromData(self, name, symbol, cid=None):
        self.name = name
        self.symbol = symbol
        self.cid = cid

    @classmethod
    def fromDB(self, itemId):
        (self.name, self.symbol) = super.load(self, itemId)
        self.cid = itemId
