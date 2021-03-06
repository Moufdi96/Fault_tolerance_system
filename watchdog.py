from watchdogClient import WatchdogClient
from clientTCP import TCPClient
import os
import threading
import time

class WatchDog:
    def __init__(self):
        
        self.client1 = WatchdogClient("primary")
        self.client2 = WatchdogClient("backup")
        self.client3 = TCPClient()   #this client is used to notify the sensor in case the primary server has crushed
        #TCPClient.freeServerAddress(2500)
        #TCPClient.freeServerAddress(2550)
        #TCPClient.freeServerAddress(3024)
        self.primary_server = 'server1'
        self.backup_server = 'server2'
        self.thread_client1 = threading.Thread(target=self.client1.connectToServer,args=['localhost',2500])
        self.thread_send1 = threading.Thread(target=self.client1.send)
        self.thread_receive1 = threading.Thread(target=self.client1.receive) 

        self.thread_client3 = threading.Thread(target=self.client3.connectToServer,args=['localhost',2550])        
        #self.thread_send3 = threading.Thread(target=self.client3.send) 
        
        self.thread_updatePrimaryServer = threading.Thread(target=self.updatePrimaryServer)

    
    '''
    def deadServer_event(self):
        #disconnect from the dead server  
        self.disconnectFromServer()
        #turn on the the backup server 
        os.system(self.primary_server+".py")
        #nominate backup server as primary server and vice versa 
        self.invertPriority()
        #connect to the new primary server (previously backup)
        #self.connectToServer()
    '''
    
    def invertPriority(self):
        self.primary_server, self.backup_server = self.backup_server, self.primary_server
   
    def updatePrimaryServer(self):
        while True:
            if self.primary_server == "server1" and self.client1.getPriority() == "backup":
                #threading.Thread(target=os.system,args=['python3 /home/moufdi/GitHubProjects/Projet_mutlithreading/server2.py']).start()
                
                threads = self.reinit_client2_threads()
                self.invertPriority()
                self.notifySensor(self.primary_server)
                self.client2.setPriority("primary")
                threads[0].start()
                threads[1].start()
                threads[2].start()
            elif self.primary_server == "server2" and self.client2.getPriority() == "backup":
                #threading.Thread(target=os.system,args=['python3 /home/moufdi/GitHubProjects/Projet_mutlithreading/server1.py']).start()
                threads = self.reinit_client1_threads()
                self.invertPriority()
                self.notifySensor(self.primary_server)
                self.client1.setPriority("primary")
                threads[0].start() 
                threads[1].start()
                threads[2].start() 

    def reinit_client1_threads(self):
        self.client1 = WatchdogClient("primary")
        thread_client1 = threading.Thread(target=self.client1.connectToServer,args=['localhost',2500])
        thread_send1 = threading.Thread(target=self.client1.send)
        thread_receive1 = threading.Thread(target=self.client1.receive) 
        return thread_client1, thread_send1, thread_receive1
    
    def reinit_client2_threads(self):
        self.client2 = WatchdogClient("primary")
        thread_client2 = threading.Thread(target=self.client2.connectToServer,args=['localhost',3024])
        thread_send2 = threading.Thread(target=self.client2.send)
        thread_receive2 = threading.Thread(target=self.client2.receive) 
        return thread_client2, thread_send2, thread_receive2

    def notifySensor(self, newPrimaryServer): #notify sensor that the current working servor has been crushed
        self.client3.send(newPrimaryServer)


    def start(self):
        self.thread_client1.start()
        self.thread_send1.start()
        self.thread_receive1.start()
        self.thread_client3.start()
        self.thread_updatePrimaryServer.start()
