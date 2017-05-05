#!/usr/bin/env python
# coding=utf-8

import pymysql.cursors
import datetime

from config import *

class MysqlDB():
    qtyPerStatement = 100
    
    def __init__(self, config):
        self.config = config
        self.configdb = ConfigDB.get(self.config.getConn())
        
        self.conn = pymysql.connect(host = self.configdb["host"],
                        user = self.configdb["user"],
                        password = self.configdb["pass"],
                        db = self.configdb["schema"],
                        charset = self.configdb["charset"],
                        cursorclass = pymysql.cursors.DictCursor)
        
    def __del__(self):
        try:
            self.conn.close()
        except:
            pass
            
    def run(self, file, data):
        self.messages = data
        
        {
            'INSERT': self.runInsert,
            'UPDATE_DUPLICATED': self.runUpdateDuplicated,
            'UPDATE': self.runUpdate,
            'UPDATE_INSERT': self.runUpdateInsert,
            'DELETE': self.runDelete
        }.get(self.config.getAction())()
    
    def runStatement(self, sql, params):
        with self.conn.cursor() as cursor:
            cursor.executemany(sql, params)
            
        self.conn.commit()
        
    def getData(self, msg, bootstrap):
        items = []
        for key, value in bootstrap.items():
            if value == '%DATE_NOW':
                items.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            elif value[:4] == '%RUN':
                # TODO
                pass
            else:
                items.append(msg[value])
                
            # TODO CONVERT TYPE
        
        return items
        
    def hasRequiredFields(self, msg):
        
        # TODO
        
        return True
    
    def runInsert(self):
        columns = [k for k,v in self.config.getBootstrap().items()]
        
        sql = "INSERT INTO " + self.config.getTable() + " (" + ",".join(columns) + ") VALUES (" + ",".join([ '%s' for s in columns ]) + ")"
        params = []
        i = 0
        for msg in self.messages:   
            if not self.hasRequiredFields(msg):
                continue
            
            params.append(self.getData(msg, self.config.getBootstrap()))
            i = i+1
            
            if i>= self.qtyPerStatement:
                self.runStatement(sql, params)
                i = 0
                params = []
            
        if i > 0:
            self.runStatement(sql, params)
        
    def runUpdateDuplicated(self):
        items = self.config.getBootstrap()
        columns = [k for k,v in items.items()]
        
        columnsUpdate = []
        for key in columns:
            if key in self.config.getBootstrapNotUpdate():
                continue
            
            columnsUpdate.append(key)
        
        sql = "INSERT INTO " + self.config.getTable() + " (" + ",".join(columns) + ") VALUES (" + ",".join([ '%s' for s in columns ]) + ") ON DUPLICATE KEY UPDATE " + ",".join([ s + '=VALUES(' + s + ')' for s in columnsUpdate ])

        params = []
        i = 0
        for msg in self.messages:   
            if not self.hasRequiredFields(msg):
                continue
            
            params.append(self.getData(msg, items))
        
            i = i+1
            
            if i>= self.qtyPerStatement:
                self.runStatement(sql, params)
                i = 0
                params = []
            
        if i > 0:
            self.runStatement(sql, params)
        
    def runUpdate(self):
        return None
        
    def runUpdateInsert(self):
        return None
        
    def runDelete(self):
        return None