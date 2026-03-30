import io
from PIL import Image


IMG_MAX_WIDTH = 50
IMG_MAX_HEIGHT = 50

ASCII_PALATTE = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def rgbToAscii(r,g,b):
    return ASCII_PALATTE[round((r+g+b)/3/255 * (len(ASCII_PALATTE)-1))]

def imgToRows(data: bytes):
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w = min(img.width, IMG_MAX_WIDTH)
    h = max(1, min(int(img.height * (w / img.width) * 0.45), IMG_MAX_HEIGHT))
    img = img.resize((w, h), Image.LANCZOS)
    rows = ""
    for y in range(h):
        row = ""
        for x in range(w):
            r,g,b = img.getpixel((x, y))
            row += rgbToAscii(r,g,b)
        rows += row+"\n"
    return rows
