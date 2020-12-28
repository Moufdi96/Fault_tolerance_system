import threading
import socket
import sys
import time
import os

class ClientTCP :
    def __init__(self,priority = "primary"):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.priority = priority
        self._opened = -1 
        self.port = 0
        self.data = ''

    def disconnectFromServer(self):
        #self.sock.shutdown()   
        self._opened = -1
        self.sock.close()
        
        #os.system('fuser -k '+ str(self.port)+'/tcp')
    
    def isDisconnected(self):
        return self.sock._closed
    
    def isConnected(self):
        return self._opened
        
    def connectToServer(self,port):
        
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', port)
        self.port = port
        print('connecting to {} port {}'.format(*server_address))
        self._opened = self.sock.connect_ex(server_address)
        #print(self.isConnected())

    def receive(self):
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                self.data = self.sock.recv(16).decode("utf-8")
                if(self.data != ''):   
                    print('received {!r} from {}'.format(self.data,self.port))

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
        time.sleep(2)
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