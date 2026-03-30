import socket
import threading
import json
import time
import config


s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#('viscous-persistent.gl.at.ply.gg',17664 )
s.bind(("::1",0))

connected = False
lastServerPing = time.time()
users = {}
timeout = 3
loadingAnimationIdx = 1

print(s.getsockname())
def sendFrame(frame):
    if time.time()-lastServerPing > timeout:
        print("Disconnected")
        global connected
        connected = False
    packet = json.dumps({"type":"frame","username":config.username,"frame":frame})
    s.sendto(packet.encode(), config.serverIP)

def ping():
    global loadingAnimationIdx
    if not connected:
        print("Connecting to "+str(config.serverIP[0])+("."*loadingAnimationIdx))
        packet = json.dumps({"type":"ping","username":config.username,"frame":"None"})
        s.sendto(packet.encode(), config.serverIP)
        loadingAnimationIdx += 1

def receive():
    global connected
    global lastServerPing
    while True:
        if s:
            packetJSON, addr = s.recvfrom(1024)
            packet = json.loads(packetJSON.decode())
            if packet["type"] == "userData":
                users[addr] = user
            elif packet["type"] == "ping":
                lastServerPing = time.time()
                connected = True
                print("Connected")
            elif packet["type"] == "error":
                lastServerPing = time.time()
                connected = True
                print("Connected")



t = threading.Thread(target=receive, daemon=True)
t.start()

