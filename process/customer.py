#!/usr/bin/env python
# coding=utf-8

from base import *
    
class Runner(Base):
    configFile = 'config/customer.json'
    
    def __init__(self):
        Base.__init__(self)
    
if __name__ == '__main__':
    Runner()