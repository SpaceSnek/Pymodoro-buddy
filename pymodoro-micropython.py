from machine import Pin, SoftI2C
import ssd1306
import time

# OLED Setup
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Button Setup
btn1 = Pin(5,  Pin.IN, Pin.PULL_UP)
btn2 = Pin(18, Pin.IN, Pin.PULL_UP)
btn3 = Pin(19, Pin.IN, Pin.PULL_UP)

def draw_topBottom():
    display.text("Pymodoro Buddy", 8, 0,  1)  # Top line
    display.text("Start Pause Stop", 0, 56, 1)  # Bottom line

def draw_CountDown(num):
    display.fill(0)
    draw_topBottom()
    display.text(str(num), 32, 28, 1)
    display.show()

display.fill(0)
draw_topBottom()
display.show()

countdown_mode = False
pause_mode = False
countdown_seconds = 3600

while True:
    hours = countdown_seconds // 3600
    minutes = (countdown_seconds % 3600) // 60
    seconds = countdown_seconds % 60
    countdown_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    draw_CountDown(countdown_str)

    if btn1.value() == 0:
        countdown_mode = True

    if countdown_mode:
        if btn2.value() == 0:
            pause_mode = True
            countdown_mode = False
        else:
            countdown_seconds -= 1
            time.sleep_ms(1000)

    if pause_mode:
        if btn2.value() == 0:
            pause_mode = False
            countdown_mode = True
        elif btn1.value() == 0:
            pause_mode = False
        else:
            time.sleep_ms(100)
