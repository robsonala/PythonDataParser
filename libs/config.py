#!/usr/bin/env python
# coding=utf-8

import json

import sys

class ProcessConfig():
    def __init__(self, file):
        with open(file) as data_file:    
            self.data = json.load(data_file)
            
    def getQueueName(self):
        return self.data['name']
            
    def getSenderThreads(self):
        return int(self.data['sender_threads'])
            
    def getListenerThreads(self):
        return int(self.data['listener_threads'])
            
    ### IN
    def getInOrderFiles(self):
        return self.data['in']['order_files']
        
    def getInFileMatch(self):
        return self.data['in']['file_match']
        
    def getInPath(self):
        return self.data['in']['new_path']
        
    def getArchivePath(self):
        return self.data['in']['archive_path']
        
    def getTypeParser(self):
        return self.data['in']['type_parser']
        
    def getIgnoreFirstLine(self):
        return self.data['in']['ignore_first_line']
        
    def getParserFields(self):
        return self.data['in']['fields']
        
    ### LISTENER
    def getListenerFormat(self):
        return self.data['listener_rules']['format']
        
    def getListenerActions(self):
        return self.data['listener_rules']['action']
        
    def getListenerDbMysql(self):
        for db in self.data['listener_rules']['mysql']:
            yield ProcessConfigDBMysql(db)
        
class ProcessConfigDBMysql():
    def __init__(self, data):
        self.data = data
    
    def getConn(self):
        return self.data['conn']
    
    def getTable(self):
        return self.data['table']
    
    def getAction(self):
        return self.data['action']
    
    def getCondition(self):
        return self.data['condition']
    
    def getBootstrap(self):
        return self.data['bootstrap']
    
    def getBootstrapNotUpdate(self):
        return self.data['bootstrap_not_update']
        
class ConfigDBMysql:
    dbs = {
        "fatdb": {
            "host": "192.232.233.227",
            "user": "robson",
            "pass": "rob123",
            "schema": "robson",
            "charset": "utf8"
        }
    }
    
    @staticmethod
    def get(name):
        return ConfigDBMysql.dbs[name]
        