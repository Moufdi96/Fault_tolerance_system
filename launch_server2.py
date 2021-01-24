from serverMachine import ServerMachine
from clientTCP import TCPClient

print('\n')
print('Killing any TCP sockets running on port 3024 ...')
TCPClient.freeServerAddress(3024)
print("\n")
server2 = ServerMachine('server2')
server2.startServer('localhost',3024,server2.receiveData)