import threading
import socket
import sys
import time
import os
from clientTCP import TCPClient

TIMEOUT = 2

class WatchdogClient(TCPClient) :
    def __init__(self,priority = "primary"):
        TCPClient.__init__(self)
        self.priority = priority

    def send(self):
        while True :
            if self.isConnected() == 0 and self.isDisconnected() == False:
                #print(self.isConnected())
                #print(self.isDisconnected())
                message = 'Are you still alive ?'
                try:
                # Send data   

                    print('sending {!r} to {}'.format(message,self.port))
                    self.sock.sendall(message.encode())
                    
                    self.start_timer()
                    #if self.timeout:
                    #    break
                except:
                    pass

    def start_timer(self):
        time.sleep(TIMEOUT)
        if self.data != 'i am alive':
            #self.timeout = True
            self.timeout_event()
        else:
            self.data = ''

    def timeout_event(self):
        self._opened = -1
        print('Oups ! primary server dead')
        self.priority = "backup"
        
        #disconnect from the dead server  
        print('disconnect from the dead server..')
        self.disconnectFromServer()

        #turn on the backup server 
        print('Switching to backup...')
        print('Turning on backup...')
        #os.system(self.primary_server+".pys") 

    def getPriority(self):
        return self.priority

    def setPriority(self,priority):
        self.priority = priority