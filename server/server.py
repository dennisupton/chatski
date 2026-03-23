import socket
import threading
import user
import json

port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', port))


print ("Server is at port %s" %(port))

ASCII_PALATTE = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def receive():
    while True:
        frame, addr = server.recvfrom(1024)
        if not user.hasUser(addr):
            print("User joined : "+ str(addr))
            user.user(addr,frame)
        else:
            user.updateUser(addr,frame)

        

t = threading.Thread(target=receive, daemon=True)
t.start()



while True:
    # send all user data to the clients
    for x in user.users:
        jsonString = json.dumps(x.dataAsDict())
        for y in user.users:
            if x.address != y.address:
                print("sent packets")
                server.sendto(jsonString.encode(), y.address)



c.close()