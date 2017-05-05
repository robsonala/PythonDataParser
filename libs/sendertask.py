#!/usr/bin/env python
# coding=utf-8

import threading
import time
import os

from preparemessage import *
from utils import *
from rabbitqueue import *

class SenderTask (threading.Thread):
    def __init__(self, queueLock, signal, config, q):
        threading.Thread.__init__(self)
        self.queueLock = queueLock
        self.config = config
        self.signal = signal
        self.q = q
        self.r = RabbitQueue(self.signal, self.config.getQueueName())
        
    def prepareMessage(self, file):
        if self.config.getTypeParser() == 'XML':
            return PrepareMessage.xml(file, self.config)
        elif self.config.getTypeParser() == 'CSV':
            return PrepareMessage.csv(file, self.config)
        elif self.config.getTypeParser() == 'PIPELINE':
            return PrepareMessage.pipeline(file, self.config)
        
    def run(self):
        while (self.signal.keep_running()):
            self.queueLock.acquire()
            if not self.q.empty():
                data = self.q.get()
                print ("processing %s" % (data))
                
                info = os.stat(os.path.join(self.config.getInPath(), data))
                
                if not os.path.isfile(os.path.join(self.config.getInPath(), data)):
                    continue
                
                os.rename(os.path.join(self.config.getInPath(), data), os.path.join(self.config.getArchivePath(), data))
                
                chunks = self.prepareMessage(os.path.join(self.config.getArchivePath(), data))
                for chunk in chunks:
                    self.r.send(Utils.structReturn(data, chunk))
            else:
                self.r.send('ping') # TODO: Verify if has message on queue before send new one
                time.sleep(1)
            self.queueLock.release()
            pass