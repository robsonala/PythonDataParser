#!/usr/bin/env python
# coding=utf-8

import threading
import os
import json

from utils import *
from rabbitqueue import *
from db import *

import sys

class ListenerTask (threading.Thread):
    def __init__(self, signal, config):
        threading.Thread.__init__(self)
        self.config = config
        self.signal = signal
        self.r = RabbitQueue(self.signal, self.config.getQueueName())
        
    def parseMsg(self, msg):
        msg = msg.decode('utf8')
        
        if msg[:4] == 'ping':
            return None
            
        if self.config.getListenerFormat() == 'JSON':
            data = json.loads(msg)
        elif self.config.getListenerFormat() == 'XML':
            # TODO
            return None
        
        return data

    def listenerCallback(self, ch, method, properties, body):
        data = self.parseMsg(body)
        self.r.checkDelivered(ch, method)
        
        if data != None:
            actions = self.config.getListenerActions()
            for action in actions:
                if action == 'mysql':
                    dbs = self.config.getListenerDbMysql()
                    for db in dbs:
                        localDb = MysqlDB(db)
                        localDb.run(data["file"], data["payload"])
                elif action =='class':
                    #TODO
                    return None
            
        
    def run(self):
        while (self.signal.keep_running()):
            self.r.listener(self.listenerCallback)