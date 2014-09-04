#!/usr/bin/env python3
import sqlite3
from os.path import expanduser
from hashlib import sha1


class SqliteItem(object):
    dbpath = expanduser('~/.bookkeepr/user.db')

    def __init__(self):
        self.con = sqlite3.connect(self.dbpath)
        self.c = self.con.cursor()

    def load(self, itemId):
        self.cr.execute(self.fromQuery, itemId)
        self.con.commit()
        return self.c.fetchone()

    ##TODO fix for updates!
    def save(self, query, data):
        self.c.execute(query, data)
        self.con.commit()
        return self.c.lastrowid


class Bill(SqliteItem):
    @classmethod
    def fromDB():
        raise NotImplemented

    @classmethod
    def fromData():
        raise NotImplemented


class Tag(SqliteItem):
    @classmethod
    def fromDB(self, tid:
        raise NotImplemented

    @classmethod
    def fromData():
        raise NotImplemented


class User(SqliteItem):
    fromQuery = 'SELECT login, password FROM users WHERE uid = ?'
    toQuery = 'INSERT INTO users (uid, login, password) VALUES (?,?,?)'

    @classmethod
    def fromDB(self, uid):
        """This is a constructor. Really."""
        this = User()
        (this.name, this.password) = super(User, self).load(this, uid)
        this.uid = uid
        return this

    @classmethod
    def fromData(self, login, password, uid=None):
        """This is a constructor. Really."""
        this = User()
        this.login = login
        self.password = sha1(password).hexdigest()
        self.uid = uid
        return this

    def toDB(self):
        data = (self.uid, self.login, self.password)
        uid = super(User, self).save(self.toQuery, data)
        self.uid = uid if self.uid is None else self.uid
        return self.uid

    def printSelf(self):
        print('User {}, password hash {}'.format(self.login, self.password))


class Currency(SqliteItem):
    fromQuery = 'SELECT name, symbol FROM currencies WHERE cid = ?'
    toQuery = 'INSERT INTO currencies (cid, name, symbol) VALUES (?,?,?)'

    #def __init__(self):
    #    super().__init__()

    @classmethod
    def fromData(self, name, symbol, cid=None):
        """This is a constructor. Really."""
        this = Currency()
        this.name = name
        this.symbol = symbol
        this.cid = cid
        return this

    @classmethod
    def fromDB(self, cid):
        """This is a constructor. Really."""
        this = Currency()
        (this.name, this.symbol) = super(Currency, self).load(this, cid)
        this.cid = cid
        return this

    def toDB(self):
        data = (self.cid, self.name, self.symbol)
        cid = super(Currency, self).save(self.toQuery, data)
        self.cid = cid if self.cid is None else self.cid
        return self.cid

    def printSelf(self):
        print('Currency {}, Symbol {}'.format(self.name, self.symbol))


if __name__ == '__main__':
    euro = Currency.fromData('Euro', '€')
    euro.printSelf()
    cid = euro.toDB()
    print('New ID: {}'.format(cid))
