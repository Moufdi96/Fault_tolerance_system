from clientThread import ClientTCP
import os
import threading
import time

TIMEOUT = 2

class WatchDog(ClientTCP):
    def __init__(self):
        ClientTCP.__init__(self)
        self.primary_down = False
        self.primary_port = 2095
        self.backup_port = 5094
        self.primary_server = 'server1'
        self.backup_server = 'server2'
        self.data = ''
        self.thread_server1 = threading.Thread(target=self.connectToServer,args=self.primary_port)
        #self.thread_server2 = threading.Thread(target=self.connectToServer,args=self.backup_port)
        #self.setTimeout(timeout)
        self.thread_send = threading.Thread(target=self.send)
        self.thread_receive = threading.Thread(target=self.receive) 
        #self.thread_timer = threading.Thread(target=self.start_timer)
        self.thread_server1.start()
        self.thread_send.start()
        self.thread_receive.start()
          
        
        
    
    #def setTimeout(self,timeout):
    #    self.timeout = timeout

    def timeout_event(self):
        print('Oups ! primary server dead')
        #disconnect from the dead server  
        print('disconnect from the dead server..')
        #self.disconnectFromServer()
       
        #nominate backup server as primary server and vice versa 
        self.invertPriority()
        #self.thread_server2.start()
        ##turn on the backup server 
        print('Switching to backup...')
        print('Turning on backup...')
        #os.system(self.primary_server+".pys")
        ##connect to backup 
        #self.connectToServer()
        print('Backup now is primary')
        

    def deadServer_event(self):
        #disconnect from the dead server  
        self.disconnectFromServer()
        #turn on the the backup server 
        os.system(self.primary_server+".py")
        #nominate backup server as primary server and vice versa 
        self.invertPriority()
        #connect to the new primary server (previously backup)
        #self.connectToServer()

    def invertPriority(self):
        self.primary_server, self.backup_server = self.backup_server, self.primary_server

    def send(self):
        while True and self.sock != None:
            message = 'Are you still alive ?'
            try:
            # Send data   
                #print(self.sock._closed)     
                #print('sending {!r}'.format(message))
                self.sock.sendall(message.encode())
                #self.thread_timer.start()
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
        
    def receive(self):
        while True:
            self.data = self.sock.recv(16).decode("utf-8")
            if(self.data != ''):   
                print('received {!r}'.format(self.data))
                #if self.data == 'i am dead':
                #    self.deadServer_event()
                #elif self.timeout :
                #    self.timeout_event()
        


w = WatchDog()