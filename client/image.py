import io
from PIL import Image
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import threading

volume = 0.0
def audio_callback(indata, frames, time, status):
    global volume
    volume = np.linalg.norm(indata) * 10
    
    
audio = sd.InputStream(
    samplerate=48000,     
    channels=1,            
    dtype='float32',      
    callback=audio_callback
)
audio.start()

subtitle = "nothing"

def listenForSubtitle():
    global subtitle
    r = sr.Recognizer()
    with sr.Microphone() as source:
        
        r.adjust_for_ambient_noise(source)
        while True:
            audio = r.listen(source)
            try:
                subtitle = r.recognize_google(audio)
            except Exception as e:
                subtitle = str(e)

subtitlesThread = threading.Thread(target=listenForSubtitle, daemon=True)
subtitlesThread.start()

IMG_MAX_WIDTH = 50
IMG_MAX_HEIGHT = 50

ASCII_PALATTE = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
dynamicShading = True
mute = False

def rgbToAscii(r,g,b, imgRange):
    global volume
    if dynamicShading:
        intensity = ((r+g+b)/3/255)/imgRange
        if not mute and volume > 8:
            intensity += volume/100
        intensity = min(intensity, 1)

    else:
        intensity = ((r+g+b)/3/255)
    return ASCII_PALATTE[round(intensity * (len(ASCII_PALATTE)-1))]

def getRange(img,h,w):
    min = 99
    max = 0
    for y in range(h):
        for x in range(w):
            r,g,b = img.getpixel((x, y))
            if (r+g+b)/3/255 > max:
                max = (r+g+b)/3/255 
            if (r+g+b)/3/255 < min:
                min = (r+g+b)/3/255
    return max - min
    
                

def imgToRows(data: bytes):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w = min(img.width, IMG_MAX_WIDTH)
    h = max(1, min(int(img.height * (w / img.width) * 0.45), IMG_MAX_HEIGHT))
    img = img.resize((w, h), Image.LANCZOS)
    imgRange = getRange(img,h,w)

    rows = ""
    for y in range(h):
        row = ""
        for x in range(w-1,0,-1):
            r,g,b = img.getpixel((x, y))
            row += rgbToAscii(r,g,b,imgRange)
        rows += row+"\n"
    rows = rows[0:len(rows)-1]
    if not subtitle == "":
        rows[len(rows)-2] = subtitles
    return rows
