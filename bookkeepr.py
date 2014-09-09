#!/usr/bin/env python3
import sqlite3
from os.path import expanduser
from hashlib import sha1


class SqliteItem(object):
    """
    Persistence.
    Define queries in classes inheriting from here, use methods, ???, profit
    """
    dbpath = expanduser('~/.bookkeepr/user.db')

    def __init__(self):
        self.con = sqlite3.connect(self.dbpath)
        self.c = self.con.cursor()

    def load(self, itemId):
        self.cr.execute(self.fromQuery, itemId)
        self.con.commit()
        return self.c.fetchone()

    def update(self, data):
        self.c.execute(self.updateQuery, data)
        return self.con.commit()

    def create(self, data):
        self.c.execute(self.createQuery, data)
        self.con.commit()
        return self.c.lastrowid


class Bill(SqliteItem):
    loadQuery = 'SELECT image, name, amount FROM bills WHERE bid = ?'
    createQuery = 'INSERT INTO bills (image, name, amount) VALUES (?,?,?)'
    updateQuery = ('UPDATE bills SET '
                   'image = ?, name = ?, amount = ? '
                   'WHERE bid = ?')

    @classmethod
    def fromDB(self, bid):
        """Another constructor."""
        obj = Bill()
        (obj.image, obj.name, obj.amount) = super(Bill, obj).load(obj, bid)
        obj.tags = ()
        obj.bid = bid
        return obj

    @classmethod
    def fromData(self, image, name, amount, bid=None):
        """Another constructor."""
        obj = Bill()
        obj.tags = ()
        obj.image = image
        obj.name = name
        obj.amount = amount
        obj.bid = bid
        return obj

    def create(self):
        data = (self.image, self.name, self.amount)
        self.bid = super(Bill, self).create(self, data)
        return self.bid

    def update(self):
        data = (self.image, self.name, self.amount, self.bid)
        super(Bill, self).update(self, data)
        return self.bid

    def save(self):
        """Save self and related data to the DB"""
        if self.bid is None:
            self.create()
            for tag in self.tags:
                tag.save()
        else:
            self.update()
            for tag in self.tags:
                tag.save()
        return self.bid


class Tag(SqliteItem):
    loadQuery = 'SELECT tag FROM tags WHERE tid = ?'
    createQuery = 'INSERT INTO tags (tag) VALUES (?)'
    updateQuery = 'UPDATE tags SET tag = ? WHERE tid = ?'

    @classmethod
    def fromDB(self, tid):
        """Mom, it's not a phase! I'm a constructor, really!"""
        obj = Tag()
        obj.tag = super(Tag, obj).load(obj, tid)
        obj.tid = tid
        return obj

    @classmethod
    def fromData(self, tag, tid=None):
        """Mom, it's not a phase! I'm a constructor, really!"""
        obj = Tag()
        obj.tag = tag
        obj.tid = tid
        return obj

    def create(self):
        data = (self.tag)
        self.tid = super(Tag, self).create(self, data)
        return self.tid

    def update(self):
        data = (self.tag, self.tid)
        super(Tag, self).update(self, data)
        return self.tid

    def save(self):
        if self.tid is None:
            return self.create()
        else:
            return self.update()


class User(SqliteItem):
    loadQuery = 'SELECT login, password FROM users WHERE uid = ?'
    createQuery = 'INSERT INTO users (login, password) VALUES (?,?)'
    updateQuery = 'UPDATE users SET login = ?, password = ? WHERE uid = ?'

    @classmethod
    def fromDB(self, uid):
        """This is a constructor. Really."""
        obj = User()
        (obj.name, obj.password) = super(User, obj).load(obj, uid)
        obj.uid = uid
        return obj

    @classmethod
    def fromData(self, login, password, uid=None):
        """This is a constructor. Really."""
        obj = User()
        obj.login = login
        obj.password = sha1(password).hexdigest()
        obj.uid = uid
        return obj

    def create(self):
        data = (self.login, self.password)
        self.uid = super(User, self).save(self, data)
        return self.uid

    def update(self):
        data = (self.login, self.password, self.uid)
        super(User, self).update(self, data)
        return self.uid

    def save(self):
        if self.uid is None:
            return self.create()
        else:
            return self.update()

    def printSelf(self):
        print('User {}, password hash {}'.format(self.login, self.password))


class Currency(SqliteItem):
    loadQuery = 'SELECT name, symbol FROM currencies WHERE cid = ?'
    createQuery = 'INSERT INTO currencies (name, symbol) VALUES (?,?)'
    updateQuery = 'UPDATE currencies SET name = ?, symbol = ? WHERE cid = ?'

    #def __init__(self):
    #    super().__init__()

    @classmethod
    def fromData(self, name, symbol, cid=None):
        """This is a constructor. Really."""
        obj = Currency()
        obj.name = name
        obj.symbol = symbol
        obj.cid = cid
        return obj

    @classmethod
    def fromDB(self, cid):
        """This is a constructor. Really."""
        obj = Currency()
        (obj.name, obj.symbol) = super(Currency, obj).load(obj, cid)
        obj.cid = cid
        return obj

    def create(self):
        data = (self.name, self.symbol)
        self.cid = super(Currency, self).create(data)
        return self.cid

    def update(self):
        data = (self.name, self.symbol, self.cid)
        super(Currency, self).update(self, data)
        return self.cid

    def save(self):
        if self.cid is None:
            return self.create()
        else:
            return self.update()

    def printSelf(self):
        print('Currency {}, Symbol {}'.format(self.name, self.symbol))

# Testing. Please stand back.
if __name__ == '__main__':
    euro = Currency.fromData('Euro', '€')
    euro.printSelf()
    cid = euro.save()
    print('New ID: {}'.format(cid))
