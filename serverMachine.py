from serverTCP import ServerTCP
import threading
from clientTCP import TCPClient 
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
            # ensuring Temporal redundancy
            res_1 = self.computeMean(self.data)
            res_2 = self.computeMean(self.data)
            if res_1 == res_2:
                print('mean value of the last {} acquired is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,res_1))
                self.store_acquired_data(PATH_STABLE_MEMORY, self.data, res_1)
            else: 
                res_3 = self.computeMean(self.data)
                # majority voting
                if res_3 == res_1:
                    print('mean value of the last {} acquired is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,res_1))
                    self.store_acquired_data(PATH_STABLE_MEMORY, self.data, res_1)
                elif res_3 == res_2:
                    print('mean value of the last {} acquired is {} :'.format(ServerTCP.SLIDING_WINDOW_LENGHT,res_2))
                    self.store_acquired_data(PATH_STABLE_MEMORY, self.data, res_2)
                else: # server failed to obtain the correct value
                    print("Service failed to produce the correct values..... " + self.server1ID + " needs to be repaired !!!")
                    print("shutting down " + self.server1ID + ".....")
                    self.sock.close()
                    TCPClient.freeServerAddress(self.server_address[1])
                    

            #print(self.data)
            
    
    def store_acquired_data(self, path, newDataVector, mean):
        saveData(path, newDataVector, mean)
        
    def set_priority(self, priority):
        self.priority = priority

    def recover_data(self):
        dataBase = loadJsonFile(PATH_STABLE_MEMORY)
        if len(dataBase) > 0: 
            self.data = dataBase[len(dataBase)-1][0]
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

    def computeMean(self,data):
        mean = np.mean(self.data)
        return mean
    
     
