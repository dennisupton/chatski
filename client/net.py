import socket
import threading
import json
import time

username = input("Enter Username : ")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

serverIP = ('127.0.0.1', 5005)#('viscous-persistent.gl.at.ply.gg',17664 )
s.bind(("",0))

connected = False
lastServerPing = time.time()
users = {}
timeout = 3

print(s.getsockname())
def sendFrame(frame):
    if time.time()-lastServerPing > timeout:
        print("Disconnected")
        global connected
        connected = False
    packet = json.dumps({"type":"frame","username":username,"frame":frame})
    s.sendto(packet.encode(), serverIP)

def ping():
    if not connected:
        print("Connecting...")
        packet = json.dumps({"type":"ping","username":username,"frame":"None"})
        s.sendto(packet.encode(), serverIP)

def receive():
    while True:
        if s:
            packetJSON, addr = s.recvfrom(1024)
            packet = json.loads(packetJSON.decode())
            if packet["type"] == "userData":
                users[addr] = user
            elif packet["type"] == "ping":
                global connected
                global lastServerPing
                lastServerPing = time.time()
                connected = True
                print("Connected")




t = threading.Thread(target=receive, daemon=True)
t.start()

