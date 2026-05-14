#!/bin/python
import spidev as SPI
import ST7789
import time
from fastapi import FastAPI

from PIL import Image,ImageDraw,ImageFont

LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam mollis sed risus ac pharetra. Aliquam ut ..."
PORT = 8000
ROTATION = 270
default_response = {
    "ok": True,
    "api": [
        "/",
        "/clear",
        "/flash",
        "/rotation/[angle]",
        "/text/[text]"
    ],
    "rotation": ROTATION
}
font = ImageFont.load_default(32)

disp = ST7789.ST7789()
disp.Init()
disp.clear()
disp.bl_DutyCycle(100)

img = Image.new("RGB", (disp.width, disp.height), "BLACK")
draw = ImageDraw.Draw(img)

def wrap_text(text):
    """
    Wraps text to fit within the max_width.
    """
    words = text.split()
    lines = [] # Holds each line in the text box
    current_line = [] # Holds each word in the current line under evaluation.

    for word in words:
        # Check the width of the current line with the new word added
        test_line = ' '.join(current_line + [word])
        width = draw.textlength(test_line, font=font)
        if width <= disp.width:
            current_line.append(word)
        else:
            # If the line is too wide, finalize the current line and start a new one
            lines.append(' '.join(current_line))
            current_line = [word]

    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines

def update(_img=img):
    global ROTATION
    disp.ShowImage(_img.rotate(ROTATION))

def clear(color="BLACK"):
    draw.rectangle([(0,0),(disp.width,disp.height)], fill=color, width = 1)

def flash():
    for i in range(0, 3):
        clear()
        update()
        clear("WHITE")
        update()
        time.sleep(0.3)
    clear()
    update()

def show_text(text):
    clear()
    lines = wrap_text(text)
    for y in range(0, len(lines)):
        draw.text((0,y*32), lines[y], fill = "WHITE", font=font)
    update()

def startup():
    flash()
    show_text(LOREM)
    time.sleep(3)
    show_text("ready")

def shutdown():
    show_text("shutting down")

startup()

app = FastAPI()

@app.get("/flash")
async def _flash():
    flash()
    return default_response | {"rotation": ROTATION}

@app.get("/text/{text}")
async def _text(text):
    show_text(text)
    return default_response | {"rotation": ROTATION}

@app.get("/rotation/{angle}")
async def _rotation(angle: int):
    if angle not in [0, 90, 180, 270]:
      return {"ok": False, "error": "angle should be one of [0, 90, 180, 270]"}
    global ROTATION, default_response
    ROTATION = angle
    update(img)
    return default_response | {"rotation": ROTATION}

@app.get("/clear")
async def _clear():
    clear()
    update()
    return default_response | {"rotation": ROTATION}

@app.get("/")
async def root():
    return default_response | {"rotation": ROTATION}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="debug")
