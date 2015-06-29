#!/usr/bin/env python
#coding=utf-8
import os
import settings
import MySQLdb
import MySQLdb.cursors
class mysql:
    def __init__(self):
        dbFilePath = settings.DB_STRING
        dbConfig = dbFilePath.strip("\n").split("/")
#         print dbConfig
        if len(dbConfig) != 5:
            raise Exception,'db string is error'
        host = dbConfig[0]
        port = dbConfig[1]
        user = dbConfig[2]
        passwd = dbConfig[3]
        db = dbConfig[4]
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=int(port), charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def fetchAll(self, sql,data=[]):
        result = []
        sql = sql % tuple(data)
#         print sql 
        if self.cursor.execute(sql):
            result = self.cursor.fetchall()
        return result
    def fetchOne(self, sql,data=[]):
        result = []
        sql = sql % tuple(data)
#         print sql 
        if self.cursor.execute(sql):
            result = self.cursor.fetchone()
        return result
    def getList(self,tableName,colums,condition,orders='',limits=''):
        sql = "SELECT "+colums+" FROM " + tableName + " WHERE 1=1"
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"='%s'"
        else:
            sql = sql + condition
        if orders !='':
            sql = sql+' order by '+orders
        if limits != '':
            sql = sql+' limit '+limits
        return self.fetchAll(sql,condition.values())
    def getOne(self,tableName,colums,condition,orders='',limits=''):
        sql = "SELECT "+colums+" FROM " + tableName + " WHERE 1=1"
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"='%s'"
        else:
            sql = sql + condition
        if orders !='':
            sql = sql+' order by '+orders
        if limits != '':
            sql = sql+' limit '+limits
        return self.fetchOne(sql,condition.values())
    def insert(self, tableName, data):
        sql = "INSERT INTO " + tableName + "("

        sql = sql + ','.join(data.keys())
        sql = sql + ") VALUES('"
        dv = [str(i) for i in data.values()]
        sql = sql + "','".join(dv)
        sql = sql + "')"
#         print sql
        status = self.cursor.execute(sql)
        self.conn.commit()
        return status
    def delete(self, tableName, condition):
        sql = "DELETE FROM " + tableName + " WHERE 1=1"
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"='%s'"
        else:
            sql = sql + condition
        sql = sql % tuple(condition.values())
#         print sql
        status = self.cursor.execute(sql)
        self.conn.commit()
        return status
    def update(self, tableName, data, condition):
        sql = "UPDATE " + tableName + " SET "
        #update data
        if  type(data) == dict:
            ts = ""
            for i in data.keys():
                ts += " , "+i+"='%s'"
            sql += ts[2:]
        else:
            sql = sql + data
            #condition
        sql = sql + " WHERE 1=1 "
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"='%s'"
        else:
            sql = sql + condition
        sql = sql % tuple(data.values()+condition.values())
#         print sql
        status = self.cursor.execute(sql)
        self.conn.commit()
        return status
    def execute(self,sql):
        status = self.cursor.execute(sql)
        self.conn.commit()
        return status

    def executeInsert(self,sql):
        status = self.cursor.execute(sql)
        # print dir(self.cursor)
        if status:
            lastrowid = self.cursor.lastrowid
        else:
            lastrowid = 0
        self.conn.commit()
        return lastrowid