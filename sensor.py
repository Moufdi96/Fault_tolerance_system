from sensorClient import SensorClient
from serverTCP import ServerTCP
import threading
import time

class Sensor:
    def __init__(self):
        self.client1 = SensorClient()
        self.client2 = SensorClient()
        self.primary_server = 'server1'
        self.backup_server = 'server2' 
        self.thread_client1 = threading.Thread(target=self.client1.connectToServer,args=['localhost',2500])
        self.thread_send1 = threading.Thread(target=self.client1.send)
        self.thread_receive1 = threading.Thread(target=self.client1.receive)

        self.thread_updateCurrentPrimaryServer = threading.Thread(target=self.updateCurrentPrimaryServer)
        
        #self.thread_client2 = threading.Thread(target=self.client2.connectToServer,args=['localhost',3024])
        #self.thread_send2 = threading.Thread(target=self.client2.send)
        #self.thread_receive2 = threading.Thread(target=self.client2.receive)
        
    #def reinit_threads(self):
    #    while True:
    #        if self.client2.isConnected() == 0:
    #            self.client1.disconnectFromServer()
    #            self.client1 = SensorClient()     
    #            thread_client1 = threading.Thread(target=self.client1.connectToServer,args=[2500])
    #            thread_send1 = threading.Thread(target=self.client1.send)
    #            thread_receive1 = threading.Thread(target=self.client1.receive)
    #            thread_client1.start()
    #            thread_send1.start()
    #            thread_receive1.start()
    #        elif

    def updateCurrentPrimaryServer(self):
        from clientTCP import TCPClient
        TCPClient.freeServerAddress(2550)
        server = ServerTCP()
        conn = server.startServer1('localhost',2550)
        print(conn)
        currentRunningServer = self.primary_server           
        while(True):
            print(currentRunningServer)
            currentRunningServer = server.receive(conn) #server.data
            if self.primary_server == 'server1' and currentRunningServer == 'server2':
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!! Oups server1 has crushed !!!!!!!!!!!!!!!!!!!!!!!!')
                print("\n")
                print('shutting down data communication with primary server (server1).....')
                self.client1.disconnectFromServer()
                self.invertPriority()
                threads = self.reinit_client2_threads()
                print('Backup server launched.... switching data communication with backup (server2).....')
                threads[0].start()
                threads[1].start()
                threads[2].start()
            elif self.primary_server == 'server2' and currentRunningServer == 'server1':
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!! Oups server2 has crushed !!!!!!!!!!!!!!!!!!!!!!!!')
                print("\n")
                print('shutting down data communication with primary server (server2).....')
                self.client2.disconnectFromServer()
                self.invertPriority()
                threads = self.reinit_client1_threads()
                print('Backup server launched.... switching data communication with backup (server1).....')
                threads[0].start()
                threads[1].start()
                threads[2].start()

                

                
    
    def invertPriority(self):
        self.primary_server, self.backup_server = self.backup_server, self.primary_server
    
    def reinit_client1_threads(self):
        self.client1 = SensorClient()
        thread_client1 = threading.Thread(target=self.client1.connectToServer,args=['localhost',2500])
        thread_send1 = threading.Thread(target=self.client1.send)
        thread_receive1 = threading.Thread(target=self.client1.receive) 
        return thread_client1, thread_send1, thread_receive1
    
    def reinit_client2_threads(self):
        self.client2 = SensorClient()
        thread_client2 = threading.Thread(target=self.client2.connectToServer,args=['localhost',3024])
        thread_send2 = threading.Thread(target=self.client2.send)
        thread_receive2 = threading.Thread(target=self.client2.receive) 
        return thread_client2, thread_send2, thread_receive2 

    def start(self):
        self.thread_client1.start()
        self.thread_send1.start()
        self.thread_receive1.start()
        self.thread_updateCurrentPrimaryServer.start()


