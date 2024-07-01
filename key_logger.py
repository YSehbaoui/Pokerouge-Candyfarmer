import threading
import time
from pynput import keyboard
from pyautogui import press
from tkinter import messagebox

log_file = "key_log.txt"
time_log_file = "time_log.txt"

key_mappings = {
    keyboard.Key.enter: 'enter',
    keyboard.Key.esc: 'esc',
    keyboard.Key.shift: 'shiftleft',
    keyboard.Key.ctrl_l: 'ctrlleft',
    keyboard.Key.ctrl_r: 'ctrlright',
    keyboard.Key.alt_l: 'altleft',
    keyboard.Key.alt_r: 'altright',
    keyboard.Key.tab: 'tab',
    keyboard.Key.backspace: 'backspace',
    keyboard.Key.delete: 'delete',
    keyboard.Key.home: 'home',
    keyboard.Key.end: 'end',
    keyboard.Key.page_down: 'pagedown',
    keyboard.Key.page_up: 'pageup',
    keyboard.Key.left: 'left',
    keyboard.Key.right: 'right',
    keyboard.Key.up: 'up',
    keyboard.Key.down: 'down',
    keyboard.Key.print_screen: 'printscreen',
    keyboard.Key.pause: 'pause',
    keyboard.Key.caps_lock: 'capslock',
    keyboard.Key.num_lock: 'numlock',
    keyboard.Key.scroll_lock: 'scrolllock',
    keyboard.Key.insert: 'insert',
    keyboard.Key.f1: 'f1',
    keyboard.Key.f2: 'f2',
    keyboard.Key.f3: 'f3',
    keyboard.Key.f4: 'f4',
    keyboard.Key.f5: 'f5',
    keyboard.Key.f6: 'f6',
    keyboard.Key.f7: 'f7',
    keyboard.Key.f8: 'f8',
    keyboard.Key.f9: 'f9',
    keyboard.Key.f10: 'f10',
    keyboard.Key.f11: 'f11',
    keyboard.Key.f12: 'f12',
    keyboard.Key.space: 'space'
}

last_time = None
stop_program = False
SAFETY_SLEEP = 0.2
lock = threading.Lock()
first_key_logged = False

record_thread = None
execute_thread = None

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
    global stop_program, listener_thread
    stop_program = False
    clear_log_file(log_file)
    clear_log_file(time_log_file)
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    return listener_thread

def execute_log_file():
    global stop_program, execute_thread
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
    # Nicht den aktuellen Thread joinen
    threading.Thread(target=stop_execution).start()

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

def start_recording():
    global record_thread
    if record_thread is None: 
        record_thread = threading.Thread(target=record_new_log_file)
        record_thread.start()
        messagebox.showinfo("Aufzeichnung", "Die Aufzeichnung hat begonnen. Drücken Sie 'Stop Recording', um zu stoppen.")
    else: 
        messagebox.showwarning("Aufzeichnung", "Es wird gerade schon aufgezeichnet.")

def stop_recording():
    global record_thread
    stop_listener()
    if record_thread is not None:
        stop_listener_explicitly()
        record_thread.join()
        record_thread = None
    messagebox.showinfo("Aufzeichnung", "Die Aufzeichnung wurde gestoppt.")

def start_execution():
    global execute_thread
    if execute_thread is None:
        execute_thread = threading.Thread(target=execute_log_file)
        execute_thread.start()
        messagebox.showinfo("Ausführung", "Die Ausführung beginnt in 5 Sekunden. Drücken Sie 'Stop Execution', um zu stoppen.")
    else:
        messagebox.showwarning("Ausführung", "Es wird gerade schon ausgeführt.")

def stop_execution():
    global execute_thread
    stop_listener()
    if execute_thread is not None:
        execute_thread.join()
        execute_thread = None
    messagebox.showinfo("Ausführung", "Die Ausführung wurde gestoppt.")
