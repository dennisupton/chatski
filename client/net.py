import socket
import threading
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverIP = ('147.185.221.23', 17362)
s.bind(('0.0.0.0', 0))

users = {}

def sendFrame(frame):
    s.sendto(frame.encode(), serverIP)

def receive():
    while True:
        if s:
            userJSON, addr = s.recvfrom(4096)
            user = json.loads(userJSON.decode())
            users[addr] = user
            

        

t = threading.Thread(target=receive, daemon=True)
t.start()
