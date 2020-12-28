from serverThread import ServerTCP

class ServerMachine(ServerTCP):

    def __init__(self, serverID):
        ServerTCP.__init__(self)
        self.server1ID = serverID
        self.priority = ''  #primary or backup 

    def process_data(self):
        pass

    def set_priority(self, priority):
        self.priority = priority
    
     
