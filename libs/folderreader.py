#!/usr/bin/env python
# coding=utf-8

import glob
import os
import threading
import time

class FolderReader(threading.Thread):
    def __init__(self, queueLock, signal, config, q):
        threading.Thread.__init__(self)
        self.queueLock = queueLock
        self.config = config
        self.signal = signal
        self.q = q
        
    def run(self):
        while (self.signal.keep_running()):
            if self.q.empty():
                self.queueLock.acquire()
                
                for i in self.config.getInFileMatch():
                    files = glob.glob(os.path.join(self.config.getInPath(), i))
                    
                    if self.config.getInOrderFiles() == True:
                        files.sort()
                    
                    for j in files:
                        info = os.path.split(j)
                        self.q.put(info[len(info)-1])
                        
                self.queueLock.release()
            else:
                time.sleep(1)
            pass