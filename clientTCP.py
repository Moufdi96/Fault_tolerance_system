import threading
import socket
import sys
import time

class TCPClient :
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._opened = -1 
        self.port = 0
        self.data = ''
        
    def connectToServer(self,port):
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', port)
        self.port = port
        print('connecting to {} port {}'.format(*server_address))
        self._opened = self.sock.connect_ex(server_address)
        #print(self.isConnected())   
        
    def disconnectFromServer(self):
        #self.sock.shutdown()   
        self._opened = -1
        self.sock.close()
        
        #os.system('fuser -k '+ str(self.port)+'/tcp')
    
    def isDisconnected(self):
        return self.sock._closed
    
    def isConnected(self):
        return self._opened

    def receive(self):
        while True:
            if self.isConnected() == 0 and self.isDisconnected() == False:
                self.data = self.sock.recv(16).decode("utf-8")
                if(self.data != ''):   
                    print('received {!r} from {}'.format(self.data,self.port))    

    def send(self):
        while True :
            if self.isConnected() == 0 and self.isDisconnected() == False:
                pass