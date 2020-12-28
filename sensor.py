from clientThread import ClientTCP

class Sensor(ClientTCP):
    def __init__(self):
        ClientTCP.__init__(self)


s = Sensor()


