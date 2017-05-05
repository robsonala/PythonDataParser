#!/usr/bin/env python
# coding=utf-8

import signal

class SignalKiller:
  kill_now = False
  
  def __init__(self):
    signal.signal(signal.SIGINT, self.send_signal)
    signal.signal(signal.SIGTERM, self.send_signal)
  
  def send_signal(self, signum, frame):
    print("Sending kill signal")
    self.kill_now = True
  
  def keep_running(self):
    return self.kill_now == False
    