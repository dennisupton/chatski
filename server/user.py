


users = []

class user:
    def __init__(self,address,frame: str,username,lastPacket):
        self.address = address
        self.frame = frame
        self.lastPacket = lastPacket
        self.username = username
        users.append(self)

    def dataAsDict(self):
        return {"address": self.address, "frame":self.frame, "username":self.username}

def hasUser(address):
    for i in users:
        if i.address == address:
            return True
    return False

def updateUser(address,frame,username,lastPacket):
    for i in users:
        if i.address == address:
            i.frame = frame
            i.username = username
            i.lastPacket = lastPacket
            
