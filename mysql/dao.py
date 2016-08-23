#!/usr/bin/env python

import pymysql
import time

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, *kwargs)
        return cls._instance

class Dao(Singleton):

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password='666666'
        self.db = 'test'
        self.charset = 'utf8'
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset=self.charset, cursorclass=pymysql.cursors.DictCursor)

    def query(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor
        except:
            return False


    def queryOne(self, sql):
        cursor = self.query(sql)
        if cursor == False:
            return False
        result = cursor.fetchone()
        return result

    def queryAll(self, sql):
        cursor = self.query(sql)
        if cursor == False:
            return False
        result = cursor.fetchall()
        return result

    #db insert
    def insert(self,table_name, data):
        sql = 'INSERT INTO `%s`(' % table_name
        if len(data) == 0:
            return False
        for i in data:
            sql += "`%s`," % i
        sql = sql.strip(',')
        sql += ') VALUES('
        for i in data:
            sql += "'%s'," % data[i]
        sql = sql.strip(',')
        sql += ')'

        return self.query(sql)

    #db update
    def update(self, table_name, data, condition):
        sql = 'UPDATE `%s` SET ' % table_name
        if len(data) == 0:
            return False
        for i in data:
            sql += "`%s`='%s'," % (i,data[i])

        sql = sql.strip(',')
        sql += " WHERE";
        for i in condition:
            sql += " `%s`='%s' AND" % (i,condition[i])
        sql = sql.strip('AND')

        return self.query(sql)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()


if __name__ == '__main__':

    dao = Dao()
    sql = "select * from hello";
    result = dao.queryAll(sql)
    condition = [];
    for item in result:
        condition.append(str(item['id']))

    sql = "update hello set name=concat(name,' w') where id in(%s)" % ','.join(condition)
    dao.query(sql)
    dao.commit()
    print(sql)