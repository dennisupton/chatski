import io
from PIL import Image


IMG_MAX_WIDTH = 50
IMG_MAX_HEIGHT = 50

ASCII_PALATTE = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
dynamicShading = True

def rgbToAscii(r,g,b, imgRange):
    if dynamicShading:
        intensity = ((r+g+b)/3/255)/imgRange
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
    return rows
