import time
import os

# Function to prompt user for the working and break durations.
def get_user_input():
    workMinutes = int(input("How long do you want to work for? (in minutes):"))
    breakMinutes = int(input("How long do you want to break for? (in minutes):"))
    return workMinutes, breakMinutes

# Silly little function to clear the screen - this is just me being dumb, this will be removed eventually
def clear_screen():
    os.system('cls')

# The math of the operation - creates our formatted timings and logic for break/work
def run_timer(seconds, label, end_prompt):
    clear_screen()
    print(label)
    while seconds >= 0:
        formatted = time.strftime("%H:%M:%S", time.gmtime(seconds))
        print(f"\r\033[KTime remaining: {formatted}\nPress Ctrl+C to stop the timer...\033[1A", end="", flush=True)
        time.sleep(1)
        seconds -= 1
    print(f"\r\033[K{end_prompt}\n\033[K", end="", flush=True)
    input()

# This function handles our looping logic, yippee!
def run_session(workMinutes, breakMinutes):
    run_timer(workMinutes * 60, "Work Session", "Press Enter to start your break...")
    run_timer(breakMinutes * 60, "Break Session", "Press Enter to start a new session...")

# Main function of  the program, called by Main to make it happen.
def main():
    workMinutes, breakMinutes = get_user_input()
    input("Press Enter to start the clock...")
    try:
        while True:
            run_session(workMinutes, breakMinutes)
    except KeyboardInterrupt:
        print("\nTimer stopped.")
        print("Pymodoro Session is over! Have a great day!")

main()
