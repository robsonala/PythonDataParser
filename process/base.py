#!/usr/bin/env python
# coding=utf-8

import sys

from basesender import *
from baselistener import *

class Base():
    configFile = None
    
    def __init__(self):
        argv = sys.argv[1:]
        action = "sender" if len(argv) == 0 else argv[0]
        
        if action == "sender":
            print("Running Sender...")
            
            BaseSender(self.configFile)
        elif action == "listener":
            print("Running Listener...")
            
            BaseListener(self.configFile)