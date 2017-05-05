#!/usr/bin/env python
# coding=utf-8

from signalkiller import *
from config import *
from listenertask import *

import threading

class BaseListener():
    def __init__(self, config_file):
        self.config = ProcessConfig(config_file)
        self.signal = SignalKiller()
        self.threads = []
            
        ## start tasks
        self.runTasks()
            
        print("Finished")
        
    def runTasks(self):
        for i in range(0, self.config.getListenerThreads()):
            thread = ListenerTask(self.signal, self.config)
            thread.start()
            self.threads.append(thread)
        
        while (self.signal.keep_running()):
            pass
        
        # Wait for all threads to complete
        for t in self.threads:
            t.join()