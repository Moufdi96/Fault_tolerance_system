import threading
import socket
import sys
import os
import time

class ServerTCP :
    data = ""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    
    def startServer(self,port):        
        # Bind the socket to the port
        os.system('fuser -k '+ str(port)+'/tcp')
        server_address = ('localhost', port)
        print('starting up on {} port {}'.format(*server_address))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)
        # Listen for incoming connections
        self.sock.listen(3)
        # Wait for a connection
        print('waiting for a connection')
        while True:
            #connection, client_address = self.sock.accept()
            serverThread = threading.Thread(target=self.receiveData,args=self.sock.accept())
            serverThread.start()

    def receiveData(self,connection,client_address):
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:  
                temp = (connection.recv(32)).decode("utf-8")  
                try:  
                    data = float(temp)
                except:
                    data = temp

                print(type(data))
                if(temp!= None):
                    if(data.__class__ == str):
                        ServerTCP.data = data.lower()
                    else:
                        ServerTCP.data = data

                    print('received from {} : {}'.format(client_address,ServerTCP.data))
                    response = 'i am alive'
                    print('sending {!r}'.format(response))
                    connection.sendall(response.encode())
        except:
            pass







