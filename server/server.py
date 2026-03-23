import socket
import threading
import user
import json
import time



TIMEOUT = 3 # seconds
log = []


port = 5005
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', port))


log.append("Server is at port %s" %(port))

def receive():
    while True:
        frame, addr = server.recvfrom(1024)
        if not user.hasUser(addr):
            log.append("User joined : "+ str(addr))
            user.user(addr,frame,time.time())
        else:
            user.updateUser(addr,frame,time.time())


t = threading.Thread(target=receive, daemon=True)
t.start()



while True:
    print("\033[2J\033[H", end="", flush=True)
    # send all user data to the clients
    for x in user.users:
        jsonString = json.dumps(x.dataAsDict())
        for y in user.users:
            if x.address != y.address:
                server.sendto(jsonString.encode(), y.address)
        if time.time()- x.lastPacket > TIMEOUT:
            log.append(str(x.address) + " left")
            user.users.remove(x)
    #Server UI
    print(str(len(user.users))+" are connected")
    print("┌───────────────────")
    for i in log:
        print("│"+i)
    print("└───────────────────")
    time.sleep(0.01)
c.close()