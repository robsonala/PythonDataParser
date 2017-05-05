#!/usr/bin/env python
# coding=utf-8

import pika
import time
import json

class RabbitQueue():
    Url = 'amqp://gzgryttx:VMo5Q5ximRrw3wtgogjFRJZhZz5ILr2t@penguin.rmq.cloudamqp.com/gzgryttx'
    
    def __init__(self, signal, name):
        self.signal = signal
        self.queueName = name
        
        self.connection = pika.BlockingConnection(pika.URLParameters(self.Url))
        self.channel = self.connection.channel()
        
    def send(self, message):
        if type(message) is not str:
            message = json.dumps(message)
        
        self.channel.basic_publish(exchange='',
                      routing_key=self.queueName,
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        
    def listener(self, fn):
        self.channel.basic_consume(fn, self.queueName)
        
        if self.signal.keep_running():
            self.channel.start_consuming()
        else:
            self.channel.stop_consuming()
            
    def checkDelivered(self, ch, method):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
        if not self.signal.keep_running():
            self.channel.stop_consuming()
        
    def __del__(self):
        self.connection.close()

