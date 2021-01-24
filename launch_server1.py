from serverMachine import ServerMachine
from clientTCP import TCPClient

print('\n')
print('Killing any TCP sockets running on port 2500 ...')
TCPClient.freeServerAddress(2500)
print("\n")
server1 = ServerMachine('server1')
server1.startServer('localhost',2500,server1.receiveData)