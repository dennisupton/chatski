


users = []

class user:
    def __init__(self,address,frame: str,lastPacket):
        self.address = address
        self.frame = frame
        self.lastPacket = lastPacket
        users.append(self)

    def dataAsDict(self):
        return {"address": self.address, "frame":self.frame.decode()}

def hasUser(address):
    for i in users:
        if i.address == address:
            return True
    return False

def updateUser(address,frame,lastPacket):
    for i in users:
        if i.address == address: # yes i know this isnt efficient but there are only gonna be like 4 users at once max 
            i.frame = frame
            i.lastPacket = lastPacket