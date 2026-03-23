import socket
import threading
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIP = ('viscous-persistent.gl.at.ply.gg',17664 )
s.bind(("",0))

users = {}
print(s.getsockname())

def sendFrame(frame):
    s.sendto(frame.encode(), serverIP)

def receive():
    while True:
        if s:
            userJSON, addr = s.recvfrom(1024)
            user = json.loads(userJSON.decode())
            users[addr] = user
            

        

t = threading.Thread(target=receive, daemon=True)
t.start()
