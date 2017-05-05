#!/usr/bin/env python
# coding=utf-8

import csv

class PrepareMessage():
    qtyPerMsg = 10
    
    @staticmethod
    def xml(filePath, config):
        yield 1
        
    @staticmethod
    def csv(filePath, config):
        columns = sorted(config.getParserFields(), key=lambda x : config.getParserFields()[x])
        
        with open(filePath) as csvfile:
            reader = csv.DictReader(csvfile, columns)
            
            if config.getIgnoreFirstLine() == True:
                next(reader)
            
            i = 0
            ret = []
            for row in reader:
                i = i+1
                ret.append(row)
                
                if i == PrepareMessage.qtyPerMsg:
                    yield ret
                    i = 0
                    ret = []
                
            if i > 0:
                yield ret
        
    @staticmethod
    def pipeline(filePath, config):
        yield 1