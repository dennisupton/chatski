import cv2
import net
import image
import time

cap = cv2.VideoCapture(0)

while True:
    if not cap.isOpened():
        print("\033[2J\033[H", end="", flush=True)
        print("Could not access webcam")

    ret, frame = cap.read()
    success, encoded = cv2.imencode('.png', frame)


    if encoded.any():
        img = image.imgToRows(encoded.tobytes())
        net.sendFrame(img)
    if len(net.users)>0:
        print("\033[2J\033[H", end="", flush=True)
        for address,user in net.users.items():
            print(user["frame"])
            print()





cap.release()
s.close()