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

def quit(sig = None, frame = None):
    net.s.close()
    print("Closed connection")
    sys.exit(0)

signal.signal(signal.SIGINT, quit)

def keybinds():
    print(input(">"))
    '''
    while True:
        key = readchar.readkey()
        if key == 'q':
            quit()
    '''
t = threading.Thread(target=keybinds, daemon=True)
# t.start()

config.checkConfig()

cap = cv2.VideoCapture(0)

while True:
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