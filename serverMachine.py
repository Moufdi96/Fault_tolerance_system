from serverTCP import ServerTCP
import threading
import numpy as np
from stableMemory import loadJsonFile, saveData

PATH_STABLE_MEMORY = "/home/moufdi/GitHubProjects/Projet_mutlithreading/stableMemory.json"

class ServerMachine(ServerTCP):
    def __init__(self, serverID):
        ServerTCP.__init__(self)
        self.server1ID = serverID
        self.priority = ''  #primary or backup 
        self.recover_data()
        #self.thread_process_data = threading.Thread(target=self.process_data)
        #self.thread_process_data.start()
    def process_data(self):
        #while True:
        if len(self.data) == ServerTCP.SLIDING_WINDOW_LENGHT:
            #continue
            mean = np.mean(self.data)
            #print(self.data)
            print('mean value of the last {} acquired is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,mean))
            self.store_acquired_data(PATH_STABLE_MEMORY, self.data, mean)
    
    def store_acquired_data(self, path, newDataVector, mean):
        saveData(path, newDataVector, mean)
        
    def set_priority(self, priority):
        self.priority = priority

    def recover_data(self):
        dataBase = loadJsonFile(PATH_STABLE_MEMORY)
        if len(dataBase) > 0: 
            self.data = dataBase[len(dataBase)-1][0]
            print(self.data)
            self.data.pop(0)

    def receiveData(self,connection,client_address):
        try:
            print('connection from', client_address)
            # Receive the data in small chunks and retransmit it
            while True:  
                temp = (connection.recv(32)).decode("utf-8")  
                #print(temp)
                
                try:  
                    data = float(temp)
                except:
                    data = temp

                #print(type(data))
                if(data!= None):
                    print('received from {} : {}'.format(client_address,data))
                    if data.__class__ == str:
                        #data = data.lower()
                        if data == 'Are you still alive ?':
                            response = 'i am alive'
                            print('sending {!r}'.format(response))
                            connection.sendall(response.encode())
                    else:
                        response = 'data received'
                        print('sending {!r}'.format(response))
                        connection.sendall(response.encode())
                        self.data.append(data)
                        print(self.data)
                        if len(self.data) >= ServerTCP.SLIDING_WINDOW_LENGHT: 
                            self.process_data()
                            self.data.pop(0)      
        except:
            pass
    
     
