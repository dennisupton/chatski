import cv2
import net
import image
import time
import readchar
import threading
import signal
import sys
import config
import ui





config.checkConfig()

keysDown = []
pause = False


def keyboardListener():
    global keysDown
    global pause
    while not pause:
        key = readchar.readchar()
        keysDown.append(key)

thread = threading.Thread(target=keyboardListener, daemon=True)
thread.start()


cap = cv2.VideoCapture(0)


while True:

    if "q" in keysDown:
        break
    if "h" in keysDown:
        ui.showHelp = not ui.showHelp
    if "d" in keysDown:
        image.dynamicShading = not image.dynamicShading
    if "c" in keysDown:
        pause = True
        config.createNewConfig()
        pause = False
    keysDown = []
    if net.connected:
        if not cap.isOpened():
            print("Could not access webcam")

        ret, frame = cap.read()
        success, encoded = cv2.imencode('.png', frame)
        if encoded.any():
            img = image.imgToRows(encoded.tobytes())
            print("\033[2J\033[H", end="", flush=True)
            net.sendFrame(img)
            ui.printUI(img,net.users)
    else:
        print("\033[2J\033[H", end="", flush=True)
        net.ping()
        time.sleep(1)


cap.release()