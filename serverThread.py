import threading
import socket
import sys
import os
import time

class ServerTCP :
    SLIDING_WINDOW_LENGHT = 3
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = []
    
    def startServer(self, IP, port, receiveFunc):        
        # Bind the socket to the port
        os.system('fuser -k '+ str(port)+'/tcp')
        server_address = (IP, port)
        print('starting up on {} port {}'.format(*server_address))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)
        # Listen for incoming connections
        self.sock.listen(3)
        # Wait for a connection
        print('waiting for a connection')
        while True:
            #connection, client_address = self.sock.accept()
            serverThread = threading.Thread(target=receiveFunc,args=self.sock.accept())
            serverThread.start()

    #def receiveData(self,connection,client_address):
    #    try:
    #        print('connection from', client_address)
    #        # Receive the data in small chunks and retransmit it
    #        while True:  
    #            temp = (connection.recv(32)).decode("utf-8")  
    #            #print(temp)
    #            
    #            try:  
    #                data = float(temp)
    #            except:
    #                data = temp
#
    #            #print(type(data))
    #            if(data!= None):
    #                if(data.__class__ == str):
    #                    data = data.lower()
    #                else:
    #                    self.data.append(data)
    #                    print(self.data)
    #                    if len(self.data) >= ServerTCP.SLIDING_WINDOW_LENGHT:  
    #                        self.data.pop(0)
    #                        #print("*****************")
    #                    
#
    #                #print('received from {} : {}'.format(client_address,data))
    #                #response = 'i am alive'
    #                #print('sending {!r}'.format(response))
    #                #connection.sendall(response.encode())
    #    except:
    #        pass

        def getData(self):
            return self.data







