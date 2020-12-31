from serverMachine import ServerMachine

server2 = ServerMachine('server2')
server2.startServer('localhost',3024,server2.receiveData)