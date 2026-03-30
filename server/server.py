import socket
import threading
import user
import json
import time

TIMEOUT = 3 # seconds
log = []

port = 5005
server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
server.bind(('::', port))


log.append(f"Server is at port {port}")

def receive():
    while True:
        packet, addr = server.recvfrom(1024)
        packet = json.loads(packet.decode())
        if packet["type"] == "ping":
            sendPing(addr)
        elif  packet["type"] == "frame":
            if not user.hasUser(addr):
                log.append(packet["username"]+" joined.")
                user.user(addr,packet["frame"],packet["username"],time.time())
            else:
                user.updateUser(addr,packet["frame"],packet["username"],time.time())
            sendPing(addr)


t = threading.Thread(target=receive, daemon=True)
t.start()

def sendUserData(data,address):
    data["type"] = "userData"
    server.sendto(json.dumps(data).encode(), address)

def sendPing(address):
    data = {"type": "ping"}
    server.sendto(json.dumps(data).encode(), address)

while True:
    print("\033[2J\033[H", end="", flush=True)
    # send all user data to the clients
    for x in user.users:
        jsonString = json.dumps(x.dataAsDict())
        for y in user.users:
            if x.address != y.address:
                sendUserData(x.dataAsDict(),y.address)

        if time.time()- x.lastPacket > TIMEOUT:
            log.append(str(x.username) + " left")
            user.users.remove(x)
    #Server UI
    print(str(len(user.users))+" are connected")
    print("┌───────────────────")
    for i in log:
        print("│"+i)
    print("└───────────────────")
    time.sleep(0.01)
c.close()