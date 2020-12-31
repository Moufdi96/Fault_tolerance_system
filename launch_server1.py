from serverMachine import ServerMachine

server1 = ServerMachine('server1')
server1.startServer('localhost',2500,server1.receiveData)