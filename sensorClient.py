import threading
import socket
import sys
import time
import os
from random import uniform
from clientTCP import TCPClient

DELAY = 4

class SensorClient(TCPClient) : 
    def __init__(self,priority = "primary"):
        TCPClient.__init__(self)
        
    def send(self):
        while True :
            self.data =''
            if self.isConnected() == 0 and self.isDisconnected() == False:
                try:
                # Send data
                    data = str(SensorClient.dataAcquisition())
                    print('sending {!r} to {}'.format(data,self.port))
                    self.sock.sendall(data.encode())
                    
                except:
                    pass
            self.start_timer()

    def start_timer(self):
        time.sleep(DELAY)

    @staticmethod
    def dataAcquisition():
        data = uniform(-10000,10000)
        return data
