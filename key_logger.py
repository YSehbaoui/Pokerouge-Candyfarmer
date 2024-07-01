import threading
import time
from pynput import keyboard
from pyautogui import press

log_file = "key_log.txt"
time_log_file = "time_log.txt"

key_mappings = {}  # Einfachheit halber leer gelassen

last_time = None
stop_program = False
SAFETY_SLEEP = 0.2
lock = threading.Lock()
first_key_logged = False

listener = None  # Der Listener wird als globale Variable definiert

def on_press(key):
    global last_time, stop_program, first_key_logged

    if stop_program:
        return False

    current_time = time.time() * 1000

    try:
        key_char = key.char
        if key_char:
            log = key_char
        else:
            log = str(key)
    except AttributeError:
        log = key_mappings.get(key, str(key))

    with lock:
        with open(log_file, "a") as f:
            f.write(log + '\n')
            print(f"{log} with ", end="")

        if not first_key_logged:
            with open(time_log_file, "a") as f:
                f.write("0\n")
                print("0ms delay")
            first_key_logged = True
        else:
            time_difference = current_time - last_time
            with open(time_log_file, "a") as f:
                f.write(f"{int(time_difference)}\n")
                print(f"{int(time_difference)}ms delay")

        last_time = current_time

def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def clear_log_file(file_path):
    with open(file_path, 'w') as file:
        pass

def record_new_log_file():
    global stop_program
    stop_program = False
    clear_log_file(log_file)
    clear_log_file(time_log_file)
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    return listener_thread

def execute_log_file():
    global stop_program
    stop_program = False
    print("Executing logfile...")
    time.sleep(5)

    print("Started Execution")
    with open(log_file, "r") as keystroke_file:
        with open(time_log_file, "r") as timestamp_file:
            for timestamp, keystroke in zip(timestamp_file, keystroke_file):
                if stop_program:
                    break
                time.sleep((int(timestamp) / 1000) + SAFETY_SLEEP) 
                keystroke = keystroke.strip()
                print(f"Pressed {keystroke} with {timestamp.strip()}ms delay")
                press(keystroke)

    print("Execution complete!")

def stop_listener():
    global stop_program
    stop_program = True
    print("Listener stopped.")

def stop_listener_explicitly():
    global listener
    global first_key_logged
    if listener is not None:
        listener.stop()
        listener = None
        first_key_logged = False
    print("Listener explicitly stopped.")
