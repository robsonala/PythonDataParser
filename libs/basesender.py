#!/usr/bin/env python
# coding=utf-8

from sendertask import *
from signalkiller import *
from config import *
from folderreader import *

import queue
import threading

class BaseSender():
    def __init__(self, config_file):
        self.config = ProcessConfig(config_file)
        self.signal = SignalKiller()
        self.threads = []
        self.queueLock = threading.Lock()
        self.q = queue.Queue(maxsize=0)
        
        ## Start folder reader
        thread = FolderReader(self.queueLock, self.signal, self.config, self.q)
        thread.start()
        self.threads.append(thread)
            
        ## start tasks
        self.runTasks()
            
        print("Finished")
        
    def runTasks(self):
        for i in range(0, self.config.getSenderThreads()):
            thread = SenderTask(self.queueLock, self.signal, self.config, self.q)
            thread.start()
            self.threads.append(thread)
        
        while (self.signal.keep_running()):
            pass
        
        # Wait for all threads to complete
        for t in self.threads:
            t.join()