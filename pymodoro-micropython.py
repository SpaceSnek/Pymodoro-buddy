from machine import Pin, SoftI2C
import ssd1306
import time

# OLED Settings
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttonsssssss
btn1 = Pin(5,  Pin.IN, Pin.PULL_UP) # Left
btn2 = Pin(18, Pin.IN, Pin.PULL_UP) # Middle
btn3 = Pin(19, Pin.IN, Pin.PULL_UP) # right

# Initialize initial states based on button presses - false on all since idle at start.
state = {
    "countdown_mode": False,
    "pause_mode": False,
    "show_image": False,
    "btn1_pressed": False,
    "btn2_pressed": False,
    "btn3_pressed": False,
}
# debounce the bouncy boys
DEBOUNCE_MS = 200
# press dictionary, this will make sure it ALWAYS registers first
last_press = {"btn1": 0, "btn2": 0, "btn3": 0}
# The (future configurable time)
countdown_seconds = 3600
# ticks instead of manual waits - waits were my blocker and this is my savior
last_tick = time.ticks_ms()

# button pressing logic with our debounce and dictionary
def on_btn1(pin):
    now = time.ticks_ms()
    if time.ticks_diff(now, last_press["btn1"]) > DEBOUNCE_MS:
        last_press["btn1"] = now
        state["btn1_pressed"] = True

def on_btn2(pin):
    now = time.ticks_ms()
    if time.ticks_diff(now, last_press["btn2"]) > DEBOUNCE_MS:
        last_press["btn2"] = now
        state["btn2_pressed"] = True

def on_btn3(pin):
    now = time.ticks_ms()
    if time.ticks_diff(now, last_press["btn3"]) > DEBOUNCE_MS:
        last_press["btn3"] = now
        state["btn3_pressed"] = True

btn1.irq(trigger=Pin.IRQ_FALLING, handler=on_btn1)
btn2.irq(trigger=Pin.IRQ_FALLING, handler=on_btn2)
btn3.irq(trigger=Pin.IRQ_FALLING, handler=on_btn3)

# load in our .bmp from aseprite (ngl i stole this shi)
def draw_bmp(filename, x, y):
    try:
        with open(filename, 'rb') as f:
            f.read(10)
            data_offset = int.from_bytes(f.read(4), 'little')
            f.read(4)
            width  = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            f.seek(data_offset)
            row_size = ((width + 31) // 32) * 4
            for row in range(height):
                f.seek(data_offset + (height - 1 - row) * row_size)
                row_data = f.read(row_size)
                for col in range(width):
                    byte = row_data[col // 8]
                    bit = (byte >> (7 - (col % 8))) & 1
                    if bit == 0:
                        display.pixel(x + col, y + row, 1)
    except OSError:
        display.text("No BMP found", 10, 28, 1)

# Draw da Display
def draw_screen(lines=[]):
    display.fill(0)
    draw_bmp("Assets/border.bmp", 0, 0)
    for text, x, y in lines:
        display.text(text, x, y, 1)
    display.show()

def draw_startScreen():
    draw_screen([("Press Start!", 15, 31)])

def draw_countdown(num):
    draw_screen([(str(num), 32, 31)])

def draw_paused(num):
    draw_screen([("PAUSED", 39, 25), (str(num), 32, 37)])

def draw_pixel_image():
    display.fill(0)
    draw_bmp("Assets/paused.bmp", 0, 0)
    display.show()

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# start our idle draw - first in the def list
draw_startScreen()

# main program loop - for now >:) 
while True:
    now = time.ticks_ms()

    # Activate countdown, set btn1 back to false, and tick
    if state["btn1_pressed"]:
        state["btn1_pressed"] = False
        state["countdown_mode"] = True
        state["pause_mode"] = False
        state["show_image"] = False
        last_tick = now  # reset tick so first second is accurate

    # Check for state of countdown and set btn2 back to false
    if state["btn2_pressed"]:
        state["btn2_pressed"] = False
        if state["countdown_mode"] or state["pause_mode"]:
            state["pause_mode"] = not state["pause_mode"]
            state["countdown_mode"] = not state["countdown_mode"]

    # Fun lil image - just showing off the display capabilities - pauses the countdown too
    if state["btn3_pressed"]:
        state["btn3_pressed"] = False
        state["show_image"] = not state["show_image"]
        if state["show_image"]:
            state["countdown_mode"] = False
            state["pause_mode"] = True
        else:
            state["countdown_mode"] = True
            state["pause_mode"] = False

    # Ticking check and logic - tldr, if tick between right now and last is more than 1k ms, tick
    if state["countdown_mode"] and not state["pause_mode"]:
        if time.ticks_diff(now, last_tick) >= 1000:
            last_tick = now
            if countdown_seconds > 0:
                countdown_seconds -= 1
            else:
                state["countdown_mode"] = False

    # Update display based on the set mode from button presses - please press button 3
    time_str = format_time(countdown_seconds)
    if state["show_image"]:
        draw_pixel_image()
    elif state["pause_mode"]:
        draw_paused(time_str)
    elif state["countdown_mode"]:
        draw_countdown(time_str)
    else:
        draw_startScreen()

    time.sleep_ms(50)