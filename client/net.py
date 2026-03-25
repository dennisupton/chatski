import socket
import threading
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIP = ('viscous-persistent.gl.at.ply.gg',17664 )
s.bind(("",0))
connected = False
users = {}

def sendFrame(frame,username):
    packet = json.dumps({"type":"frame","username":username,"frame":frame})
    s.sendto(packet.encode(), serverIP)

def ping(username):
    packet = json.dumps({"type":"ping","username":username,"frame":"None"})
    s.sendto(packet.encode(), serverIP)

def receive():
    while True:
        if s:
            userJSON, addr = s.recvfrom(1024)
            user = json.loads(userJSON.decode())
            users[addr] = user
            

        

t = threading.Thread(target=receive, daemon=True)
t.start()
