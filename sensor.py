from sensorClient import SensorClient
import threading
import time



class Sensor:
    def __init__(self):
        self.client1 = SensorClient()
        self.client2 = SensorClient()
        thread_client1 = threading.Thread(target=self.client1.connectToServer,args=['localhost',2500])
        thread_send1 = threading.Thread(target=self.client1.send)
        thread_receive1 = threading.Thread(target=self.client1.receive)
        thread_client1.start()
        thread_send1.start()
        thread_receive1.start()

        thread_client2 = threading.Thread(target=self.client2.connectToServer,args=['localhost',3024])
        thread_send2 = threading.Thread(target=self.client2.send)
        thread_receive2 = threading.Thread(target=self.client2.receive)
        thread_client2.start()
        thread_send2.start()
        thread_receive2.start()

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


    
            
Sensor()


