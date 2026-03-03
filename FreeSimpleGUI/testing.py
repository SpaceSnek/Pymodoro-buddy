# VERY ROUGH SAMPLE IMPLEMENTATION OF A GUI TYPE DISPLAY - Focusing mimicking an actual OLED display (128x64 (they are cheap on amazon)) for development purposes.

import FreeSimpleGUI as sg
import time
import math

# Create faux OLED Display for testing Graph drawing purposes.
FOLED_Width = 128
FOLED_Height = 64
FOLED_Scale = 1 # Need to look into having scale adjust all elements to size up or down for readability.

# Generate our actual layout design for the window. we set our graph background to black to emulate that of an OLED disaply, buttons at the bottom are purposefully simple to represent the future hardware implementation.
col_layout = [
    [sg.Graph(
        canvas_size=(FOLED_Width * FOLED_Scale, FOLED_Height * FOLED_Scale),
        graph_bottom_left=(0, 0),
        graph_top_right=(FOLED_Width, FOLED_Height),
        background_color='black',
        key='-GRAPH-'
    )],
    [sg.Button('S', button_color=('white','black'), size=(1,1)), sg.Button('P', button_color=('white','black'), size=(1,1)), sg.Button('Q', button_color=('white','black'), size=(1,1))]
]
# Generatre the layout and center in the window.
wincol_layout = [[sg.Col(col_layout, element_justification='center', justification='center', background_color='#DA70D6')]]

# Creates our window with the above layout and add background styling to mimick the future 3d printed case color - still not decided on what color the case will be. Sekiguchi genetics vibes perhaps?
window = sg.Window('Pymodoro Timer', wincol_layout, background_color='#DA70D6', no_titlebar=True)
window.finalize()

# Set up the basic timer - no user input....YET
timer_length = 120  # 2 minutes
running = False
graph = window['-GRAPH-']

# Actual brains, does the math for our timer and then updates the display / timer based on events near the bottome - this can CERTAINLY be cleaned up a lil bit :) 
while True:
    # HH:MM:SS format for the countdown - using f strings for easier formatting for mysefl.
    hours   = int(timer_length // 3600)
    minutes = int((timer_length % 3600) // 60)
    seconds = int(timer_length % 60)
    formatted_Time = f"{hours:02}:{minutes:02}:{seconds:02}"

    # Erase everything and redraw the screen with updated infromation from our formatted time
    graph.erase()
    graph.draw_text('Pymodoro Timer', location=(FOLED_Width//2, FOLED_Height - 8), color='white', font='VT323 8')
    graph.draw_text(formatted_Time, location=(FOLED_Width//2, FOLED_Height//2), color='white', font='VT323 12')

    # Wait for user input, once running, update every second.
    event, values = window.read(timeout=1000 if running else None)

    # Event handler - this checks for our button presses and updates the timer appropriately as well as generating a pop up for when the timer is out.
    if event == sg.WIN_CLOSED or event == 'Q':
        break
    if running:
        timer_length = max(0, math.ceil(end_time - time.time()))
    if timer_length == 0:
        sg.popup("Time's up!", title="Pymodoro Timer", background_color='black', text_color='white')
    if event == 'S':
        end_time = time.time() + timer_length
        running = True
    if event == 'P':
        if running:
            timer_length = max(0, math.ceil(end_time - time.time()))
            running = False
        else:
            end_time = time.time() + timer_length
            running = True

window.close()